import struct


CHUNK_STRING_POOL = 0x0001
CHUNK_START_TAG = 0x0102
CHUNK_END_TAG = 0x0103


def read_u16(data, offset):
    if offset + 2 > len(data):
        raise ValueError("Dados insuficientes")

    return struct.unpack_from("<H", data, offset)[0]


def read_u32(data, offset):
    if offset + 4 > len(data):
        raise ValueError("Dados insuficientes")

    return struct.unpack_from("<I", data, offset)[0]


def read_utf8_length(data, offset):
    if offset >= len(data):
        raise ValueError("String UTF-8 inválida")

    first = data[offset]
    offset += 1

    if first & 0x80:
        if offset >= len(data):
            raise ValueError("String UTF-8 inválida")

        second = data[offset]
        offset += 1

        length = ((first & 0x7F) << 8) | second

    else:
        length = first

    return length, offset


def read_utf8(data, offset):
    """
    Lê uma string UTF-8 da String Pool.
    """

    _, offset = read_utf8_length(
        data,
        offset
    )

    byte_length, offset = read_utf8_length(
        data,
        offset
    )

    end = offset + byte_length

    if end > len(data):
        raise ValueError("String UTF-8 excede o arquivo")

    raw = data[offset:end]

    text = raw.decode(
        "utf-8",
        errors="replace"
    )

    return text, end + 1


def read_utf16(data, offset):
    """
    Lê uma string UTF-16LE da String Pool.
    """

    length = read_u16(
        data,
        offset
    )

    offset += 2

    if length & 0x8000:

        second = read_u16(
            data,
            offset
        )

        offset += 2

        length = (
            ((length & 0x7FFF) << 16)
            | second
        )

    byte_length = length * 2

    end = offset + byte_length

    if end > len(data):
        raise ValueError(
            "String UTF-16 excede o arquivo"
        )

    raw = data[offset:end]

    text = raw.decode(
        "utf-16le",
        errors="replace"
    )

    return text, end + 2


def parse_string_pool(data, offset):
    """
    Extrai a String Pool do Android Binary XML.
    """

    if offset + 28 > len(data):
        return [], offset

    chunk_type = read_u16(
        data,
        offset
    )

    header_size = read_u16(
        data,
        offset + 2
    )

    chunk_size = read_u32(
        data,
        offset + 4
    )

    if chunk_type != CHUNK_STRING_POOL:
        return [], offset

    string_count = read_u32(
        data,
        offset + 8
    )

    flags = read_u32(
        data,
        offset + 16
    )

    strings_start = read_u32(
        data,
        offset + 20
    )

    offsets_base = (
        offset + header_size
    )

    offsets = []

    for index in range(string_count):

        position = (
            offsets_base
            + index * 4
        )

        if position + 4 > len(data):
            break

        offsets.append(
            read_u32(
                data,
                position
            )
        )

    strings_base = (
        offset + strings_start
    )

    is_utf8 = bool(
        flags & 0x00000100
    )

    strings = []

    for string_offset in offsets:

        position = (
            strings_base
            + string_offset
        )

        if position >= len(data):

            strings.append("")
            continue

        try:

            if is_utf8:

                text, _ = read_utf8(
                    data,
                    position
                )

            else:

                text, _ = read_utf16(
                    data,
                    position
                )

        except Exception:

            text = ""

        strings.append(text)

    return (
        strings,
        offset + chunk_size
    )


def get_string(strings, index):

    if index < 0:
        return ""

    if index >= len(strings):
        return ""

    return strings[index]


def parse_manifest(data):
    """
    Analisa AndroidManifest.xml em formato AXML.

    A análise é exclusivamente estática.
    """

    if len(data) < 8:
        raise ValueError("Manifest muito pequeno")

    strings, position = parse_string_pool(data, 8)

    if not strings:
        raise ValueError(
            "String Pool do AXML não encontrada"
        )

    permissions = []
    package_name = None
    version_code = None
    version_name = None
    application_name = None
    activities = []

    while position + 8 <= len(data):

        try:
            chunk_type = read_u16(data, position)
            header_size = read_u16(
                data,
                position + 2
            )
            chunk_size = read_u32(
                data,
                position + 4
            )
        except ValueError:
            break

        if chunk_size < 8:
            break

        if position + chunk_size > len(data):
            break

        # START_TAG
        if chunk_type == CHUNK_START_TAG:

            if header_size >= 16:

                name_index = read_u32(
                    data,
                    position + 20
                )

                name = get_string(
                    strings,
                    name_index
                )

                attribute_start = read_u16(
                    data,
                    position + 24
                )

                attribute_size = read_u16(
                    data,
                    position + 26
                )

                attribute_count = read_u16(
                    data,
                    position + 28
                )

                # attributeStart é relativo
                # ao início da extensão do elemento.
                attributes_offset = (
                    position
                    + 16
                    + attribute_start
                )

                attributes = []

                if attribute_size < 20:
                    attribute_size = 20

                for index in range(attribute_count):

                    attr_offset = (
                        attributes_offset
                        + index * attribute_size
                    )

                    if attr_offset + 20 > len(data):
                        break

                    attr_name_index = read_u32(
                        data,
                        attr_offset + 4
                    )

                    attr_value_string = read_u32(
                        data,
                        attr_offset + 8
                    )

                    attr_type = read_u32(
                        data,
                        attr_offset + 12
                    )

                    attr_data = read_u32(
                        data,
                        attr_offset + 16
                    )

                    attr_name = get_string(
                        strings,
                        attr_name_index
                    )

                    if attr_value_string != 0xFFFFFFFF:

                        attr_value = get_string(
                            strings,
                            attr_value_string
                        )

                    elif (
                        (attr_type >> 24) == 0x03
                    ):

                        attr_value = get_string(
                            strings,
                            attr_data
                        )

                    else:

                        attr_value = str(
                            attr_data
                        )

                    attributes.append(
                        (
                            attr_name,
                            attr_value
                        )
                    )

                if name == "manifest":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if attr_name == "package":
                            package_name = attr_value

                        elif attr_name == "versionName":
                            version_name = attr_value

                        elif attr_name == "versionCode":
                            version_code = attr_value

                elif name == "uses-permission":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if (
                            attr_name == "name"
                            and attr_value
                        ):

                            if attr_value not in permissions:
                                permissions.append(
                                    attr_value
                                )

                elif name == "application":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if attr_name == "name":
                            application_name = attr_value

                elif name == "activity":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if attr_name == "name":

                            if attr_value not in activities:
                                activities.append(
                                    attr_value
                                )

        position += chunk_size

    return {
        "package": package_name,
        "version_code": version_code,
        "version_name": version_name,
        "application": application_name,
        "activities": activities,
        "permissions": sorted(
            permissions
        )
    }

    # Os primeiros 8 bytes pertencem
    # ao chunk XML principal.
    #
    # A String Pool começa no offset 8
    # neste formato de AXML.

    strings, position = parse_string_pool(
        data,
        8
    )

    if not strings:

        raise ValueError(
            "String Pool do AXML não encontrada"
        )

    permissions = []

    package_name = None
    version_code = None
    version_name = None
    application_name = None

    activities = []

    while position + 8 <= len(data):

        try:

            chunk_type = read_u16(
                data,
                position
            )

            header_size = read_u16(
                data,
                position + 2
            )

            chunk_size = read_u32(
                data,
                position + 4
            )

        except ValueError:

            break

        if chunk_size < 8:
            break

        if position + chunk_size > len(data):
            break

        if chunk_type == CHUNK_START_TAG:

            if header_size >= 16:

                name_index = read_u32(
                    data,
                    position + 20
                )

                name = get_string(
                    strings,
                    name_index
                )

                attribute_start = read_u16(
                    data,
                    position + 24
                )

                attribute_size = read_u16(
                    data,
                    position + 26
                )

                attribute_count = read_u16(
                    data,
                    position + 28
                )

                attributes_offset = (
                    position
                    + attribute_start
                )

                attributes = []

                if attribute_size < 20:
                    attribute_size = 20

                for index in range(
                    attribute_count
                ):

                    attr_offset = (
                        attributes_offset
                        + index * attribute_size
                    )

                    if attr_offset + 20 > len(data):
                        break

                    attr_name_index = read_u32(
                        data,
                        attr_offset + 4
                    )

                    attr_value_string = read_u32(
                        data,
                        attr_offset + 8
                    )

                    attr_type = read_u32(
                        data,
                        attr_offset + 12
                    )

                    attr_data = read_u32(
                        data,
                        attr_offset + 16
                    )

                    attr_name = get_string(
                        strings,
                        attr_name_index
                    )

                    if attr_value_string != 0xFFFFFFFF:

                        attr_value = get_string(
                            strings,
                            attr_value_string
                        )

                    elif (
                        (attr_type >> 24)
                        == 0x03
                    ):

                        attr_value = get_string(
                            strings,
                            attr_data
                        )

                    else:

                        attr_value = str(
                            attr_data
                        )

                    attributes.append(
                        (
                            attr_name,
                            attr_value
                        )
                    )

                if name == "manifest":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if attr_name == "package":

                            package_name = (
                                attr_value
                            )

                        elif attr_name == "versionName":

                            version_name = (
                                attr_value
                            )

                        elif attr_name == "versionCode":

                            version_code = (
                                attr_value
                            )

                elif name == "uses-permission":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if (
                            attr_name == "name"
                            and attr_value
                        ):

                            if (
                                attr_value
                                not in permissions
                            ):

                                permissions.append(
                                    attr_value
                                )

                elif name == "application":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if attr_name == "name":

                            application_name = (
                                attr_value
                            )

                elif name == "activity":

                    for (
                        attr_name,
                        attr_value
                    ) in attributes:

                        if attr_name == "name":

                            if attr_value not in activities:

                                activities.append(
                                    attr_value
                                )

        position += chunk_size

    return {
        "package": package_name,
        "version_code": version_code,
        "version_name": version_name,
        "application": application_name,
        "activities": activities,
        "permissions": sorted(
            permissions
        )
    }


def permission_description(permission):

    descriptions = {

        "android.permission.INTERNET":
            "Permite acesso à Internet.",

        "android.permission.ACCESS_NETWORK_STATE":
            "Permite consultar o estado da rede.",

        "android.permission.ACCESS_WIFI_STATE":
            "Permite consultar informações da rede Wi-Fi.",

        "android.permission.ACCESS_FINE_LOCATION":
            "Permite acesso à localização precisa.",

        "android.permission.ACCESS_COARSE_LOCATION":
            "Permite acesso à localização aproximada.",

        "android.permission.READ_SMS":
            "Permite leitura de mensagens SMS.",

        "android.permission.RECEIVE_SMS":
            "Permite receber mensagens SMS.",

        "android.permission.SEND_SMS":
            "Permite enviar mensagens SMS.",

        "android.permission.READ_CONTACTS":
            "Permite leitura dos contatos.",

        "android.permission.WRITE_CONTACTS":
            "Permite modificar contatos.",

        "android.permission.CAMERA":
            "Permite acesso à câmera.",

        "android.permission.RECORD_AUDIO":
            "Permite acesso ao microfone.",

        "android.permission.POST_NOTIFICATIONS":
            "Permite enviar notificações.",

        "android.permission.BLUETOOTH":
            "Permite operações relacionadas ao Bluetooth.",

        "android.permission.BLUETOOTH_CONNECT":
            "Permite conexão com dispositivos Bluetooth.",

        "android.permission.BLUETOOTH_SCAN":
            "Permite procurar dispositivos Bluetooth.",

        "android.permission.READ_EXTERNAL_STORAGE":
            "Permite leitura do armazenamento em versões compatíveis.",

        "android.permission.WRITE_EXTERNAL_STORAGE":
            "Permite gravação no armazenamento em versões compatíveis.",
    }

    return descriptions.get(
        permission,
        "Permissão Android declarada pelo aplicativo."
    )


def show_manifest(info):

    print("\nMANIFEST")
    print("──────────────────────────────────────────")

    package_name = info.get(
        "package"
    )

    version_code = info.get(
        "version_code"
    )

    version_name = info.get(
        "version_name"
    )

    application = info.get(
        "application"
    )

    activities = info.get(
        "activities",
        []
    )

    permissions = info.get(
        "permissions",
        []
    )

    if package_name:

        print(
            f"[+] Pacote: {package_name}"
        )

    if version_name:

        print(
            f"[+] Versão: {version_name}"
        )

    if version_code:

        print(
            f"[+] Version Code: {version_code}"
        )

    if application:

        print(
            f"[+] Application: {application}"
        )

    print(
        f"[+] Activities: {len(activities)}"
    )

    print("\nPERMISSÕES")
    print("──────────────────────────────────────────")

    if not permissions:

        print(
            "[✓] Nenhuma permissão encontrada."
        )

    else:

        print(
            f"[!] Permissões encontradas: "
            f"{len(permissions)}"
        )

        for permission in permissions:

            print(
                f"\n[!] {permission}"
            )

            print(
                f"    {permission_description(permission)}"
            )

    print("\n⚠️ IMPORTANTE")
    print(
        "Informações obtidas somente do Manifest."
    )

    print(
        "A análise do Manifest é exclusivamente estática."
    )


def extract_permissions(data):

    info = parse_manifest(
        data
    )

    return info.get(
        "permissions",
        []
    )


def show_permissions(permissions):

    print("\nPERMISSÕES DO MANIFEST")
    print("──────────────────────────────────────────")

    if not permissions:

        print(
            "[✓] Nenhuma permissão Android encontrada."
        )

        return

    print(
        f"[!] Permissões encontradas: "
        f"{len(permissions)}"
    )

    for permission in permissions:

        print(
            f"\n[!] {permission}"
        )

        print(
            f"    {permission_description(permission)}"
        )

    print("\n⚠️ IMPORTANTE")

    print(
        "Permissões não significam malware."
    )

    print(
        "A análise do Manifest é exclusivamente estática."
    )
