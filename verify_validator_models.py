import os
from bitmind.synthetic_image_generation.synthetic_image_generator import SyntheticImageGenerator
from bitmind.constants import DIFFUSER_NAMES, IMAGE_ANNOTATION_MODEL, TEXT_MODERATION_MODEL
import bittensor as bt

def is_model_cached(model_name):
    """
    Check if the specified model is cached by looking for its directory in the Hugging Face cache.
    """
    cache_dir = os.path.expanduser('~/.cache/huggingface/')
    # Format the directory name correctly by replacing each slash with double dashes
    
    model_dir = f"models--{model_name.replace('/', '--')}"

    # Construct the full path to where the model directory should be
    model_path = os.path.join(cache_dir, model_dir)

    # Check if the model directory exists
    if os.path.isdir(model_path):
        bt.logging.info(f"Model {model_name} is already cached in {model_path}. Skipping...")
        return True
    else:
        bt.logging.info(f"Model {model_name} not cached in {model_path}.")
        return False


def main():
    synthetic_image_generator = SyntheticImageGenerator(prompt_type='annotation',
                                                        use_random_diffuser=True,
                                                        diffuser_name=None)
    
    # Check and load annotation and moderation models if not cached
    if not is_model_cached(IMAGE_ANNOTATION_MODEL) or not is_model_cached(TEXT_MODERATION_MODEL):
        synthetic_image_generator.image_annotation_generator.load_models()
        synthetic_image_generator.image_annotation_generator.clear_gpu()
    
    # Initialize and load diffusers if not cached
    for model_name in DIFFUSER_NAMES:
        if not is_model_cached(model_name):
            synthetic_image_generator = SyntheticImageGenerator(prompt_type='annotation',
                                                                use_random_diffuser=False,
                                                                diffuser_name=model_name)
            synthetic_image_generator.load_diffuser(model_name)
            synthetic_image_generator.clear_gpu()

if __name__ == "__main__":
    main()
