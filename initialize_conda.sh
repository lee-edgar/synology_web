#!/bin/bash

# 이 파일에 실행 권한을 부여합니다 (옵션)
chmod +x /volume1/synology/synology/synology_web/initialize_conda.sh

# Conda 초기화
source /volume1/synology/synology/miniconda3/etc/profile.d/conda.sh

# Conda 환경 활성화 (예: 'sysnology' 환경)
conda activate sysnology
