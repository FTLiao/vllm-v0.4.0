import asyncio
from functools import partial
from typing import Dict, List

from vllm.executor.single_gpu_executor import GPUExecutor
from vllm.sequence import SequenceGroupMetadata


class GPUExecutorAsync(GPUExecutor):

    async def execute_model_async(
        self,
        seq_group_metadata_list: List[SequenceGroupMetadata],
        blocks_to_swap_in: Dict[int, int],
        blocks_to_swap_out: Dict[int, int],
        blocks_to_copy: Dict[int, List[int]],
    ):
        output = await asyncio.get_event_loop().run_in_executor(
            None,
            partial(self.driver_worker.execute_model,
                    seq_group_metadata_list=seq_group_metadata_list,
                    blocks_to_swap_in=blocks_to_swap_in,
                    blocks_to_swap_out=blocks_to_swap_out,
                    blocks_to_copy=blocks_to_copy))
        return output

    async def check_health(self) -> None:
        # GPUExecutor will always be healthy as long as
        # it's running.
        return
