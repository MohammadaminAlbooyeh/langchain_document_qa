import aiofiles
from pathlib import Path


async def save_upload_file(upload_file, destination: str | Path) -> Path:
    dest = Path(destination)
    dest.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(dest, "wb") as f:
        content = await upload_file.read()
        await f.write(content)
    return dest


async def read_file_content(file_path: str | Path) -> str:
    path = Path(file_path)
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        return await f.read()


async def delete_file(file_path: str | Path):
    path = Path(file_path)
    if path.exists():
        path.unlink()


def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()


def ensure_dir(path: str | Path):
    Path(path).mkdir(parents=True, exist_ok=True)
