import zc.buildout
import zc.recipe.egg


class Recipe(object):

    def _process_list(self, value):
        if isinstance(value, list):
            return value

        else:
            if '\n' in value:
                return [v.strip() for v in value.split('\n') if v.strip()]
            else:
                return value.split()

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = {}
        self.options['files'] = self._process_list(options.get('files', []))
        self.options['directories'] = self._process_list(options.get('directories', []))
        self.options['recipe'] = options['recipe']

        if not self.options['files'] and not self.options['directories']:
            raise zc.buildout.UserError(
                'You need to add "files" or "directories" option in order '
                'to copy something to Amazon S3'
            )

        if 'AWS_ACCESS_KEY_ID' not in options or not options.get('AWS_ACCESS_KEY_ID', ''):
            raise zc.buildout.UserError(
                'AWS_ACCESS_KEY_ID option is mandatory to upload '
                'files to S3. Please provide it in the recipe options'
            )

        if 'AWS_SECRET_ACCESS_KEY' not in options or not options.get('AWS_SECRET_ACCESS_KEY', ''):
            raise zc.buildout.UserError(
                'AWS_SECRET_ACCESS_KEY option is mandatory to upload '
                'files to S3. Please provide it in the recipe options'
            )

        if 'AWS_BUCKET_NAME' not in options or not options.get('AWS_BUCKET_NAME', ''):
            raise zc.buildout.UserError(
                'AWS_BUCKET_NAME option is mandatory to upload '
                'files to S3. Please provide it in the recipe options'
            )

        self.options['AWS_ACCESS_KEY_ID'] = options.get('AWS_ACCESS_KEY_ID', '')
        self.options['AWS_SECRET_ACCESS_KEY'] = options.get('AWS_SECRET_ACCESS_KEY', '')
        self.options['AWS_BUCKET_NAME'] = options.get('AWS_BUCKET_NAME', '')
        self.options['overwrite'] = zc.buildout.buildout.bool_option(options, 'overwrite', default=False)

    def install(self):
        self.egg = zc.recipe.egg.Egg(self.buildout, self.options['recipe'], self.options)
        backup_name = self.name
        reqs = [(backup_name, 'cs.recipe.s3backup.main', 'backup')]
        executable = self.buildout['buildout']['executable']
        dest = self.buildout['buildout']['bin-directory']
        orig_distributions, working_set = self.egg.working_set(
            ['cs.recipe.s3backup', 'zc.buildout', 'zc.recipe.egg'])
        script_arguments = """filepaths=%(filepaths)s,
            directories=%(directories)s,
            AWS_ACCESS_KEY_ID='%(AWS_ACCESS_KEY_ID)s',
            AWS_SECRET_ACCESS_KEY='%(AWS_SECRET_ACCESS_KEY)s',
            AWS_BUCKET_NAME='%(AWS_BUCKET_NAME)s',
            overwrite=%(overwrite)s""" % dict(
                filepaths=self.options['files'],
                directories=self.options['directories'],
                AWS_ACCESS_KEY_ID=self.options['AWS_ACCESS_KEY_ID'],
                AWS_SECRET_ACCESS_KEY=self.options['AWS_SECRET_ACCESS_KEY'],
                AWS_BUCKET_NAME=self.options['AWS_BUCKET_NAME'],
                overwrite=self.options['overwrite'],
            )
        scripts = zc.buildout.easy_install.scripts(
            reqs=reqs,
            working_set=working_set,
            executable=executable,
            dest=dest,
            arguments=script_arguments
        )
        return scripts
