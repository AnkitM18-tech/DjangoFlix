```python


class CourseGrade():
    student -> FK(student)
    course -> FK(course)


class CourseAttendance():
    student -> FK(student)
    course -> FK(course)
    datetime -> DateTime


class Course():
    students -> M2M( )
    # course_obj.coursegrade_set.all()
    # course_obj.courseattendence_set.all(0)

class Parent():
    name
    # parent_obj.student_set.all()

class Student():
    mother = FK(parent, related_name='mother')
    father = FK(parent, related_name='father')
    # student.course_set.all()
    # student.coursegrade_set.all()
    # student.father
    # student.mother
```
















```
Playlist_a = PlayList.objects.first()

```
## Add to ManyToMany
```python
video_a = Video.objects.first()
Playlist_a.videos.add(video_a)
```

## Remove from ManyToMany
```python
video_a = Video.objects.first()
Playlist_a.videos.remove(video_a)
```


## Set (or reset) ManyToMany
```python
video_qs = Video.objects.all()
Playlist_a.videos.set(video_qs)
```


## Clear ManyToMany
```python
Playlist_a.videos.clear()
```

## Queryset from ManyToMany
```python
Playlist_a.videos.all()
```





## PlayList of PlayLists


```python

from playlists.models import PlayList

the_office = PlayList.objects.create(title='The Office Series')
# featured video / videos / 

season_1 = PlayList.objects.create(title='The Office Series Season 1', parent=the_office, order=1)
# featured video / videos / 

season_2 = PlayList.objects.create(title='The Office Series Season 2', parent=the_office, order=2)
# featured video / videos / 

season_3 = PlayList.objects.create(title='The Office Series Season 3', parent=the_office, order=3)
# featured video / videos / 

shows = PlayList.objects.filter(parent__isnull=True)
show = PlayList.objects.get(id=1)
# seasons = PlayList.objects.filter(parent=show)
```