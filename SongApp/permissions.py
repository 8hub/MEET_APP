from rest_framework import permissions

class IsPlaylistCreator(permissions.BasePermission):
  """
  Only allow creators of a playlist to modify it.
  """

  def has_object_permission(self, request, view, obj):
    # Write permissions are only allowed to the creator of the playlist.
    return obj.creator == request.user
  
class IsSongOwner(permissions.BasePermission):
  """
  Only allow creators of a song to modify it.
  """

  def has_object_permission(self, request, view, obj):
    # Write permissions are only allowed to the creator of the song.
    return obj.creator == request.user