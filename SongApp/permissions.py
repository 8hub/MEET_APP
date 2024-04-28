from rest_framework import permissions

class IsPlaylistCreator(permissions.BasePermission):
  """
  Only allow creators of a playlist to modify it.
  """
  def has_permission(self, request, view):
    return request.user and request.user.is_authenticated
  
  def has_object_permission(self, request, view, obj):
    # Write permissions are only allowed to the creator of the playlist.
    return obj.created_by == request.user
  
class IsSongOwner(permissions.BasePermission):
  """
  Only allow creators of a song to modify it.
  """
  def has_permission(self, request, view):
    return request.user and request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    # Write permissions are only allowed to the creator of the song.
    return obj.added_by == request.user