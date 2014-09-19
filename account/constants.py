
# Constants for user role.
JOB_SEEKER = 'seeker'
RECRUITER = 'recruiter'

EXPERIENCE_CHOICES = (('1', '1'),
                      ('2', '2'),
                      ('3', '3'),
                      ('4', '4'),
                      ('5', '5'),
                      ('6', '6'),
                      ('7', '7'),
                      ('8', '8'),
                      ('9', '9'),
                      ('10', '10'),
                      ('11', '11'),)

YEAR_EXPERIENCE = tuple([('0', 'Fresher')] + list(EXPERIENCE_CHOICES))
MONTH_EXPERIENCE = tuple([('0', 'Months')] + list(EXPERIENCE_CHOICES))

CTC_RANGE = tuple([ ('%s' %x, '%s' %y) for x, y in enumerate(xrange(0, 100))])

YES_NO_CHOICES = (('Y', 'Yes'),
                    ('N', 'No')
                    )

GENDER_CHOICES = (('F', 'Female'),
                  ('M', 'Male'))