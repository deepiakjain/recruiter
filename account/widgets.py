
import os
from PIL import Image
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

# from project import
from account.models import JobSeeker

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):

            image_url = value.url
            file_name=str(value)

            # defining the size
            size='100x100'
            x, y = [int(x) for x in size.split('x')]
            try:
                # defining the filename and the miniature filename
                filehead, filetail = os.path.split(value.path)
                basename, format = os.path.splitext(filetail)
                miniature = basename + '_' + size + format
                filename = value.path
                miniature_filename = os.path.join(filehead, miniature)
                filehead, filetail = os.path.split(value.url)
                miniature_url = filehead + '/' + miniature

                # make sure that the thumbnail is a version of the current original sized image
                if os.path.exists(miniature_filename) and \
                                os.path.getmtime(filename) > os.path.getmtime(miniature_filename):
                    os.unlink(miniature_filename)

                # if the image wasn't already resized, resize it
                if not os.path.exists(miniature_filename):
                    image = Image.open(filename)
                    image.thumbnail([x, y], Image.ANTIALIAS)
                    try:
                        image.save(miniature_filename, image.format, quality=100, optimize=1)
                    except:
                        image.save(miniature_filename, image.format, quality=100)

                output.append(u' <div><a href="%s" target="_blank"><img src="%s" alt="%s" /></a></div>' %\
                              (miniature_url, miniature_url, miniature_filename))
            except:
                pass

        # remove clear, change and other extra inputs
        output.append(u'<input id="%s" name="%s" type="file" />' % (attrs['id'], name))

        #super_output = super(AdminFileWidget, self).render(name, value, attrs)

        #output.append(super_output[super_output.find('e: ')+3:super_output.find('/></p')+2])
        return mark_safe(u''.join(output))


class AdminResumeWidget(AdminFileWidget):

    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            jobseeker = get_object_or_404(JobSeeker, resume=value)

            file_name = str(value).split('/')[-1]

            output.append(u'<a href="%s" target="_blank" style="text-decoration: none;">%s</a>' %
                          (reverse('download_uuid_file', args=[jobseeker.file_uuid]), file_name))

        output.append(u'<input id="%s" name="%s" type="file" %s/>' % (attrs['id'], name, '' if value else 'required' ))

        return mark_safe(u''.join(output))
