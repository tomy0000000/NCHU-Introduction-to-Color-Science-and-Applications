import struct


def ieee_single_decode(number: str) -> float:
    bins = [number[i : i + 8] for i in range(0, len(number), 8)]
    packed = int("".join(bins), 2).to_bytes(4, byteorder="big")
    decoded = struct.unpack("!f", packed)[0]
    return round(decoded, 4)


if __name__ == "__main__":
    with open("sideinforbina.txt") as input_f, open(
        "sideinfordeci.txt", "w"
    ) as output_f:
        for line in input_f:
            encoded = line.rstrip()
            decoded = ieee_single_decode(encoded)
            output_f.write(f"{decoded:.4f}\n")
