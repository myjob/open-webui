import sys
import os
import asyncio
from pathlib import Path

# Setup paths
BACKEND_DIR = "/home/job/a/open-webui/backend"
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

# Mock environment for testing
# We import directly to avoid triggering open_webui.__init__ which requires uvicorn
TOOLS_DIR = os.path.join(BACKEND_DIR, "open_webui", "tools")
if TOOLS_DIR not in sys.path:
    sys.path.append(TOOLS_DIR)

async def main():
    print("Testing celex_timeline tool...")
    
    try:
        # Import directly
        import celex_timeline
        from celex_timeline import Tools
        
        tool = Tools()
        celex_id = "CELEX-32000D0146"
        
        print(f"Requesting timeline for {celex_id}...")
        
        # Mock event emitter
        async def mock_emitter(event):
            print(f"Event: {event}")
            
        result = await tool.get_celex_timeline(celex_id, __event_emitter__=mock_emitter)
        
        print("\n--- Result ---")
        print(result[:500] + "..." if len(result) > 500 else result)
        print("\n--- End Result ---")
        
        if "Error" in result and "timeline" not in result:
             print("Test FAILED with error")
             sys.exit(1)
        else:
             print("Test PASSED")

    except Exception as e:
        print(f"Test crashed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
