#!/usr/bin/env python3
"""
Filter GeoJSON file to only include King County zip codes
This will significantly reduce the file size for easier GitHub upload
"""

import json
import os

def filter_king_county_geojson():
    """Filter the GeoJSON file to only include King County features"""
    
    input_file = "MapData/Zipcodes_for_King_County_and_Surrounding_Area_(Shorelines)___zipcode_shore_area.geojson"
    output_file = "MapData/King_County_Zipcodes.geojson"
    
    print("🗺️  Filtering GeoJSON file to King County only...")
    print(f"📁 Input: {input_file}")
    print(f"📁 Output: {output_file}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        return False
    
    try:
        # Read the original GeoJSON file
        print("📖 Reading GeoJSON file...")
        with open(input_file, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
        
        print(f"📊 Original features: {len(geojson_data['features'])}")
        
        # Filter to only King County features
        king_county_features = []
        for feature in geojson_data['features']:
            if feature.get('properties', {}).get('COUNTY_NAME') == 'King County':
                king_county_features.append(feature)
        
        print(f"📊 King County features: {len(king_county_features)}")
        
        # Create new GeoJSON with only King County features
        filtered_geojson = {
            "type": "FeatureCollection",
            "features": king_county_features
        }
        
        # Write the filtered GeoJSON
        print("💾 Writing filtered GeoJSON file...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_geojson, f, indent=2)
        
        # Get file sizes
        original_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
        filtered_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        
        print(f"📏 Original file size: {original_size:.2f} MB")
        print(f"📏 Filtered file size: {filtered_size:.2f} MB")
        print(f"📉 Size reduction: {((original_size - filtered_size) / original_size * 100):.1f}%")
        
        print(f"✅ Successfully created: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing GeoJSON: {e}")
        return False

def update_demo_html():
    """Update demo.html to use the new filtered GeoJSON file"""
    
    print("🔧 Updating demo.html to use filtered GeoJSON...")
    
    try:
        # Read demo.html
        with open('demo.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the GeoJSON file path
        old_path = "MapData/Zipcodes_for_King_County_and_Surrounding_Area_(Shorelines)___zipcode_shore_area.geojson"
        new_path = "MapData/King_County_Zipcodes.geojson"
        
        if old_path in content:
            content = content.replace(old_path, new_path)
            
            # Write back to demo.html
            with open('demo.html', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Updated demo.html to use filtered GeoJSON file")
            return True
        else:
            print("⚠️  GeoJSON path not found in demo.html")
            return False
            
    except Exception as e:
        print(f"❌ Error updating demo.html: {e}")
        return False

def main():
    """Main function"""
    print("🚀 King County GeoJSON Filter")
    print("=" * 40)
    
    # Filter the GeoJSON file
    if filter_king_county_geojson():
        # Update demo.html
        update_demo_html()
        
        print("\n🎉 Filtering complete!")
        print("📝 Next steps:")
        print("   1. The filtered file is much smaller and should upload easily")
        print("   2. Try running the deployment script again:")
        print("      python deploy_to_github.py")
        print("   3. Or use the GitHub web interface with the smaller files")
    else:
        print("\n❌ Filtering failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
