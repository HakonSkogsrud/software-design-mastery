from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Image:
    filename: str
    width: int
    height: int


def resize_image(
    image: Image,
    width: int,
    height: int,
) -> Image:
    print(
        f"Resizing {image.filename} "
        f"from {image.width}x{image.height} "
        f"to {width}x{height}"
    )

    return replace(
        image,
        width=width,
        height=height,
    )


def main() -> None:
    image = Image(
        filename="hotel-room.jpg",
        width=2400,
        height=1600,
    )

    resized_image = resize_image(
        image,
        width=1200,
        height=800,
    )

    print()
    print(
        f"Result: {resized_image.filename} "
        f"({resized_image.width}x{resized_image.height})"
    )


if __name__ == "__main__":
    main()
