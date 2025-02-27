#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools
extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_18'

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/sm7635-common',
    'hardware/qcom-caf/sm7635',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/xiaomi/sm7635-common',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libagmclient',
        'libagmmixer',
        'vendor.qti.hardware.pal@1.0-impl',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/etc/camera/amethyst_enhance_motiontuning.xml',
        'vendor/etc/camera/amethyst_motiontuning.xml',
    ): blob_fixup().regex_replace('xml=version', 'xml version'),
    (
        'vendor/etc/camera/pureShot_parameter.xml',
        'vendor/etc/camera/pureView_parameter.xml',
    ): blob_fixup().regex_replace(r'=([0-9]+)>', r'="\1">'),
    'vendor/lib64/libcamximageformatutils.so': blob_fixup().replace_needed(
        'vendor.qti.hardware.display.config-V2-ndk_platform.so',
        'vendor.qti.hardware.display.config-V2-ndk.so',
    ),
}

module = ExtractUtilsModule(
    'amethyst',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm7635-common', module.vendor
    )
    utils.run()
