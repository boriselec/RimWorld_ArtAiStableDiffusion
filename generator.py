#!/usr/bin/env python
from types import SimpleNamespace
import gc
import stablediffusion


def generate_loop(job_queue, curr_rq, startup_args):
    while True:
        args = SimpleNamespace(device=startup_args.device,
                               model=startup_args.model,
                               half=startup_args.half,
                               height=startup_args.height,
                               width=startup_args.width,
                               steps=startup_args.steps,
                               token='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',
                               skip=True,
                               seed=519762248,
                               scale=7.5,
                               strength=0.75,
                               image=None,
                               image_scale=None,
                               negative_prompt=None,
                               scheduler=None,
                               xformers_memory_efficient_attention=False,
                               attention_slicing=False,
                               mask=None)
        try:
            job = job_queue.get()
            curr_rq.value = job.rq
            args.prompt = job.art_desc
            pipeline = stablediffusion.stable_diffusion_pipeline(args)
            stablediffusion.stable_diffusion_inference(pipeline, job.rq)
        except Exception as e:
            print(e, flush=True)
            pass
        del pipeline
        del args
        gc.collect()
        curr_rq.value = None
