from django.conf import settings

__author__ = 'mm'

DEFAULT_SLO_THRESHOLD = 1000 * 1000 * 100  # 100MB
DEFAULT_SLO_CHUNK_SIZE = 1000 * 1000 * 50  # 50MB


def make_context(param_url, slo_url, file_url, force_filename, filename,
                 element_id, element_name,):

    slo_threshold = getattr(settings, 'DSD_SLO_THRESHOLD',
                            DEFAULT_SLO_THRESHOLD)

    slo_chunk_size = getattr(settings, 'DSD_SLO_CHUNK_SIZE',
                             DEFAULT_SLO_CHUNK_SIZE)

    return {
            'param_url': param_url,
            'slo_url': slo_url,
            'file_url': file_url,
            'force_filename': force_filename,
            'filename': filename,
            'element_id': element_id,
            'element_name': element_name,
            'DSD_SLO_THRESHOLD': slo_threshold,
            'DSD_SLO_CHUNK_SIZE': slo_chunk_size
    }