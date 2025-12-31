import asyncio
from PyQt6.QtCore import QThread, pyqtSignal
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus
)

async def get_all_media_sessions_async():
    try:
        manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        sessions = manager.get_sessions()
        
        result = []
        for session in sessions:
            try:
                media_properties = await session.try_get_media_properties_async()
                playback_info = session.get_playback_info()
                
                is_playing = playback_info.playback_status == GlobalSystemMediaTransportControlsSessionPlaybackStatus.PLAYING
                
                result.append({
                    "id": session.source_app_user_model_id,
                    "title": media_properties.title or "",
                    "artist": media_properties.artist or "",
                    "is_playing": is_playing,
                })
            except Exception:
                continue
                
        return result
    except Exception as e:
        print(f"Error getting media sessions: {e}")
        return []


async def media_action_async(action, app_id=None):
    try:
        manager = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        sessions = manager.get_sessions()
        
        if not sessions:
            return
            
        target_session = None
        if app_id:
            for s in sessions:
                if s.source_app_user_model_id == app_id:
                    target_session = s
                    break
        
        if not target_session and sessions:
            target_session = sessions[0]
            
        if not target_session:
            return
            
        if action == "play_pause":
            await target_session.try_toggle_play_pause_async()
        elif action == "next":
            await target_session.try_skip_next_async()
        elif action == "prev":
            await target_session.try_skip_previous_async()
            
    except Exception as e:
        print(f"Error performing media action: {e}")

class MediaWorker(QThread):
    media_sessions_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.running = True
        self.loop = None

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.loop.run_until_complete(self._poll_media())
        self.loop.close()

    async def _poll_media(self):
        while self.running:
            try:
                sessions = await get_all_media_sessions_async()
                self.media_sessions_changed.emit(sessions)
            except Exception as e:
                print(f"Media Worker Error: {e}")
            
            await asyncio.sleep(1)

    def stop(self):
        self.running = False
        self.wait()

    def perform_action(self, action, app_id=None):
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(media_action_async(action, app_id), self.loop)
