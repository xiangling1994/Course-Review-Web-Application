c = ''
    with open('/Users/WZ/Documents/djangop/viewcourse/course_collection/course(withprof).csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                c, created = course.objects.get_or_create(
                    courseid=row[0],
                    coursetitle=row[1],
                    subject=row[2],
                    university='Dalhousie University',
                )
            if len(row) == 1:
                p, created = professor.objects.get_or_create(
                    course = c,
                    full_name = row[0],
                )
                '''
                p = professor()
                p.course = c
                p.full_name = row[0]
                p.save()
                '''
