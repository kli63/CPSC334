import os
from pathlib import Path
import shutil
import json
from linedraw import vectorize, makesvg  # Import the specific functions we need

class ComponentVectorizer:
    def __init__(self):
        # Define paths relative to project root
        self.PROJECT_ROOT = Path(__file__).parent.parent.parent
        self.INPUT_BASE_DIR = self.PROJECT_ROOT / "assets" / "images" / "components"
        self.OUTPUT_BASE_DIR = self.PROJECT_ROOT / "assets" / "data" / "components"

        # Define quadrants
        self.QUADRANTS = ['q1', 'q2', 'q3', 'q4']

    def setup_directories(self):
        """Create output directory structure if it doesn't exist."""
        if self.OUTPUT_BASE_DIR.exists():
            shutil.rmtree(self.OUTPUT_BASE_DIR)
        
        for quadrant in self.QUADRANTS:
            json_dir = self.OUTPUT_BASE_DIR / quadrant / "json"
            svg_dir = self.OUTPUT_BASE_DIR / quadrant / "svg"
            json_dir.mkdir(parents=True, exist_ok=True)
            svg_dir.mkdir(parents=True, exist_ok=True)

    def process_components(self):
        """Process all components in each quadrant directory."""
        self.setup_directories()
        
        for quadrant in self.QUADRANTS:
            input_dir = self.INPUT_BASE_DIR / quadrant
            
            if not input_dir.exists():
                print(f"Warning: Input directory {input_dir} does not exist!")
                continue
                
            print(f"\nProcessing components in {quadrant}...")
            
            # Get all image files in the quadrant directory
            image_files = [f for f in input_dir.glob("*") if f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.bmp')]
            
            if not image_files:
                print(f"No images found in {input_dir}")
                continue
            
            for image_file in image_files:
                print(f"Vectorizing {image_file.name}...")
                
                try:
                    # Generate vectors
                    lines = vectorize(
                        str(image_file),
                        resolution=1024,
                        draw_contours=4, 
                        repeat_contours=1, 
                        draw_hatch=False, 
                        repeat_hatch=0
                    )
                    
                    if not lines:
                        print(f"  No lines generated for {image_file.name}")
                        continue

                    # Save SVG
                    svg_path = self.OUTPUT_BASE_DIR / quadrant / "svg" / f"{image_file.stem}.svg"
                    with open(svg_path, 'w') as f:
                        f.write(makesvg(lines))

                    # Save JSON
                    json_path = self.OUTPUT_BASE_DIR / quadrant / "json" / f"{image_file.stem}.json"
                    with open(json_path, 'w') as f:
                        json.dump(lines, f, indent=4)
                        
                    print(f"  Successfully processed {image_file.name}")
                    
                except Exception as e:
                    print(f"  Error processing {image_file.name}: {str(e)}")

def main():
    vectorizer = ComponentVectorizer()
    vectorizer.process_components()
    print("\nVectorization complete!")

if __name__ == "__main__":
    main()