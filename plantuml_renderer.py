import re
from pathlib import Path
from plantuml import PlantUML

def extract_plantuml_code(text: str) -> str:
    match = re.search(r'```plantuml\n(.*?)\n```', text, re.DOTALL)
    return match.group(1).strip() if match else ""

# Use public PlantUML server (PNG output)
plantuml = PlantUML(url="http://www.plantuml.com/plantuml/img/")

def create_plantuml_image(plantuml_code: str, output_image_path: Path):
    # Write UML code to a temp file
    from tempfile import NamedTemporaryFile

    with NamedTemporaryFile("w+", suffix=".puml", delete=False, encoding="utf-8") as tmp_file:
        tmp_file.write(f"@startuml\n{plantuml_code}\n@enduml\n")
        tmp_file_path = Path(tmp_file.name)

    # Ensure output folder exists
    output_image_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate the image into the results folder
    plantuml.processes_file(str(tmp_file_path))

    # Move generated image from temp location to desired output path
    generated_img = tmp_file_path.with_suffix(".png")
    if generated_img.exists():
        generated_img.rename(output_image_path)

    # Clean up temp .puml file
    tmp_file_path.unlink(missing_ok=True)