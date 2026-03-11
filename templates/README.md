# BiaPy Templates

This directory contains local YAML template files for BiaPy workflows, replacing the remote URLs that were previously used.

## Directory Structure

```text
templates/
├── classification/
│   ├── 2d_classification.yaml
│   └── 3d_classification.yaml
├── semantic_segmentation/
│   ├── 2d_semantic_segmentation.yaml
│   └── 3d_semantic_segmentation.yaml
├── instance_segmentation/
│   ├── 2d_instance_segmentation.yaml
│   └── 3d_instance_segmentation.yaml
├── detection/
│   ├── 2d_detection.yaml
│   └── 3d_detection.yaml
├── denoising/
│   ├── 2d_denoising.yaml
│   └── 3d_denoising.yaml
├── super_resolution/
│   ├── 2d_super-resolution.yaml
│   └── 3d_sr.yaml
├── self_supervised/
│   ├── 2d_self_supervised.yaml
│   └── 3d_self_supervised.yaml
└── image_to_image/
    ├── 2d_image_to_image.yaml
    └── 3d_image_to_image.yaml
```

## Template Mapping

The following task keys map to their corresponding template files:

- `cls2d` → `classification/2d_classification.yaml`
- `cls3d` → `classification/3d_classification.yaml`
- `seg2d` → `semantic_segmentation/2d_semantic_segmentation.yaml`
- `seg3d` → `semantic_segmentation/3d_semantic_segmentation.yaml`
- `inst2d` → `instance_segmentation/2d_instance_segmentation.yaml`
- `inst3d` → `instance_segmentation/3d_instance_segmentation.yaml`
- `det2d` → `detection/2d_detection.yaml`
- `det3d` → `detection/3d_detection.yaml`
- `denoise2d` → `denoising/2d_denoising.yaml`
- `denoise3d` → `denoising/3d_denoising.yaml`
- `sr2d` → `super_resolution/2d_super-resolution.yaml`
- `sr3d` → `super_resolution/3d_sr.yaml`
- `ssl2d` → `self_supervised/2d_self_supervised.yaml`
- `ssl3d` → `self_supervised/3d_self_supervised.yaml`
- `i2i2d` → `image_to_image/2d_image_to_image.yaml`
- `i2i3d` → `image_to_image/3d_image_to_image.yaml`

## Template Configuration

Each template contains the basic configuration structure for BiaPy workflows:

- **SYSTEM**: GPU configuration, workers, random seed
- **MODEL**: Architecture settings, checkpoint loading
- **DATA**: Patch size, paths for training/validation/test data
- **TRAIN**: Training parameters (epochs, batch size, optimizer, learning rate)
- **TEST**: Testing configuration and metrics
- **AUGMENTOR**: Data augmentation settings
- **PATHS**: File paths and result directories

## Customization

You can modify these templates to suit your specific needs:

1. **Default patch sizes**: 256x256x1 for 2D tasks, 64x64x64x1 for 3D tasks
2. **Default architecture**: UNet (can be changed to UNETR, ResUNet, etc.)
3. **Default training parameters**: 100 epochs, ADAMW optimizer, 1e-4 learning rate
4. **Task-specific metrics**:
   - Classification: accuracy
   - Segmentation: IoU
   - Detection: mAP
   - Other tasks: Default or empty metrics

## Usage

The `biapy_tool()` function in `py_tools.py` automatically loads the appropriate template based on the task type. You can also specify a custom template directory using the `local_template_dir` parameter.

## Benefits of Local Templates

1. **Reliability**: No dependency on external URLs that may become unavailable
2. **Speed**: Faster loading since no network requests are needed
3. **Customization**: Easy to modify templates for specific project needs
4. **Version control**: Templates are tracked with your project code
5. **Offline capability**: Works without internet connection