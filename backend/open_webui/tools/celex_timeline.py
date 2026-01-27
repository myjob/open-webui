"""
Celex Timeline Generator Tool

This tool integrates the TimelineTableAgent from celex-facts to generate timeline tables for given CELEX IDs.
"""
import sys
import logging
from typing import Callable, Any

# Add the celex-facts source directory to the system path to allow importing its modules.
# We rely on an absolute path as per the implementation plan.
CELEX_FACTS_PATH = "/home/job/a/celex-facts/src"
if CELEX_FACTS_PATH not in sys.path:
    sys.path.append(CELEX_FACTS_PATH)

# from open_webui.tools import Tools as BaseTools
from pydantic import BaseModel, Field

class Tools:
    def __init__(self):
        pass

    async def get_celex_timeline(
        self,
        celex_id: str,
        __user__: dict = {},
        __event_emitter__: Callable[[Any], Any] = None
    ) -> str:
        """
        Generates a timeline table for a specific CELEX ID using the Celex Timeline Agent.
        
        :param celex_id: The CELEX ID to generate a timeline for (e.g., 'CELEX-32000D0146').
        :return: A markdown formatted table containing the timeline of events.
        """
        try:
            # Import here to avoid loading it if the tool isn't used, and ensuring sys.path is set.
            from agents.TimelineTableAgent import TimelineTableAgent
            
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Generating timeline for {celex_id}...",
                            "done": False,
                        },
                    }
                )

            # Initialize the agent
            # We use the default model configuration from the agent class
            agent = TimelineTableAgent()
            
            # Generate the timeline
            result = agent.generate_timeline(celex_id)
            
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Timeline generated for {celex_id}",
                            "done": True,
                        },
                    }
                )

            return result

        except ImportError as e:
            return f"Error: Could not import TimelineTableAgent. Please ensure celex-facts is available at {CELEX_FACTS_PATH}. Details: {e}"
        except Exception as e:
            # logging.exception(f"Error generating timeline for {celex_id}: {e}")
            return f"Error generating timeline for {celex_id}: {str(e)}"
