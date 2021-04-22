import struct


def ieee_single_encode(number: float) -> str:
    packed = struct.pack("!f", number)
    unpacked = [f"{b:b}".rjust(8, "0") for b in packed]
    encoded = "".join(unpacked)
    return encoded


if __name__ == "__main__":
    with open("sideinfordeci.txt") as input_f, open(
        "sideinforbina.txt", "w"
    ) as output_f:
        for line in input_f:
            number = float(line.rstrip())
            encoded = ieee_single_encode(number)
            output_f.write(f"{encoded}\n")
