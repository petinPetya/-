def decode_base64(ref_nm):
    import base64
    try:
        padding_needed = (4 - len(ref_nm) % 4) % 4
        padded_string = ref_nm + b'=' * padding_needed
        ref_nm = base64.b64decode(padded_string).decode('utf-8')
        return ref_nm
    except (TypeError, ValueError) as e:
        print(f"Ошибка при декодировании: {e}")
        return None