# SPDX-License-Identifier: Apache-2.0

import numpy as np

import onnx

from ..base import Base
from . import expect


class Split(Base):
    @staticmethod
    def export_1d() -> None:
        input = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]).astype(np.float32)

        node = onnx.helper.make_node(
            "Split",
            inputs=["input"],
            outputs=["output_1", "output_2", "output_3"],
            axis=0,
        )

        expected_outputs = [
            np.array([1.0, 2.0]).astype(np.float32),
            np.array([3.0, 4.0]).astype(np.float32),
            np.array([5.0, 6.0]).astype(np.float32),
        ]
        expect(
            node,
            inputs=[input],
            outputs=[y for y in expected_outputs],
            name="test_split_equal_parts_1d",
        )

        split = np.array([2, 4]).astype(np.int64)
        node = onnx.helper.make_node(
            "Split",
            inputs=["input", "split"],
            outputs=["output_1", "output_2"],
            axis=0,
        )

        expected_outputs = [
            np.array([1.0, 2.0]).astype(np.float32),
            np.array([3.0, 4.0, 5.0, 6.0]).astype(np.float32),
        ]
        expect(
            node,
            inputs=[input, split],
            outputs=[y for y in expected_outputs],
            name="test_split_variable_parts_1d",
        )

    @staticmethod
    def export_2d() -> None:
        input = np.array(
            [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]]
        ).astype(np.float32)

        node = onnx.helper.make_node(
            "Split", inputs=["input"], outputs=["output_1", "output_2"], axis=1
        )

        expected_outputs = [
            np.array([[1.0, 2.0, 3.0], [7.0, 8.0, 9.0]]).astype(np.float32),
            np.array([[4.0, 5.0, 6.0], [10.0, 11.0, 12.0]]).astype(np.float32),
        ]

        expect(
            node,
            inputs=[input],
            outputs=[y for y in expected_outputs],
            name="test_split_equal_parts_2d",
        )

        split = np.array([2, 4]).astype(np.int64)
        node = onnx.helper.make_node(
            "Split",
            inputs=["input", "split"],
            outputs=["output_1", "output_2"],
            axis=1,
        )

        expected_outputs = [
            np.array([[1.0, 2.0], [7.0, 8.0]]).astype(np.float32),
            np.array([[3.0, 4.0, 5.0, 6.0], [9.0, 10.0, 11.0, 12.0]]).astype(
                np.float32
            ),
        ]

        expect(
            node,
            inputs=[input, split],
            outputs=[y for y in expected_outputs],
            name="test_split_variable_parts_2d",
        )

    @staticmethod
    def export_default_values() -> None:
        input = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]).astype(np.float32)

        # If axis is not specified, split is applied on default axis 0
        node = onnx.helper.make_node(
            "Split", inputs=["input"], outputs=["output_1", "output_2", "output_3"]
        )

        expected_outputs = [
            np.array([1.0, 2.0]).astype(np.float32),
            np.array([3.0, 4.0]).astype(np.float32),
            np.array([5.0, 6.0]).astype(np.float32),
        ]
        expect(
            node,
            inputs=[input],
            outputs=[y for y in expected_outputs],
            name="test_split_equal_parts_default_axis",
        )

        split = np.array([2, 4]).astype(np.int64)
        node = onnx.helper.make_node(
            "Split", inputs=["input", "split"], outputs=["output_1", "output_2"]
        )

        expected_outputs = [
            np.array([1.0, 2.0]).astype(np.float32),
            np.array([3.0, 4.0, 5.0, 6.0]).astype(np.float32),
        ]
        expect(
            node,
            inputs=[input, split],
            outputs=[y for y in expected_outputs],
            name="test_split_variable_parts_default_axis",
        )

    @staticmethod
    def export_zero_size_splits() -> None:
        input = np.array([]).astype(np.float32)

        # Split emtpy tensor to tensors of size zero
        split = np.array([0, 0, 0]).astype(np.int64)
        node = onnx.helper.make_node(
            "Split",
            inputs=["input", "split"],
            outputs=["output_1", "output_2", "output_3"],
        )

        expected_outputs = [
            np.array([]).astype(np.float32),
            np.array([]).astype(np.float32),
            np.array([]).astype(np.float32),
        ]
        expect(
            node,
            inputs=[input, split],
            outputs=[y for y in expected_outputs],
            name="test_split_zero_size_splits",
        )
