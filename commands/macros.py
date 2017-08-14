from commands.base.command import Command
from models import Meme


class MacroSet(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = 'set'
        self.help = 'Agrega o actualiza un macro'
        self.owner_only = True

    async def handle(self, message, cmd):
        if len(cmd.args) < 2:
            await cmd.answer('Formato: !set <nombre> <contenido>')
            return

        meme_name = cmd.args[0]
        meme_value = ' '.join(cmd.args[1:])

        meme, created = Meme.get_or_create(name=meme_name)
        meme.content = meme_value
        meme.save()

        if created:
            msg = 'Macro **{name}** creado'.format(name=meme_name)
            self.bot.log.info('Macro %s creado con valor: "%s"', meme_name, meme_value)
        else:
            msg = 'Macro **{name}** actualizado'.format(name=meme_name)
            self.bot.log.info('Macro %s actualizado a: "%s"', meme_name, meme_value)

        await cmd.answer(msg)


class MacroUnset(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = 'unset'
        self.help = 'Elimina un macro'
        self.owner_only = True

    async def handle(self, message, cmd):
        if len(cmd.args) < 1:
            await cmd.answer('Formato: !unset <nombre>')
            return

        meme_name = cmd.args[0]

        try:
            meme = Meme.get(name=meme_name)
            meme.delete_instance()
            msg = 'Macro **{name}** eliminado'.format(name=meme_name)
            await cmd.answer(msg)
            self.bot.log.info('Macro %s eliminado', meme_name)
        except Meme.DoesNotExist:
            msg = 'El macro **{name}** no existe'.format(name=meme_name)
            await cmd.answer(msg)

        await cmd.answer(msg)


class MacroList(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = 'list'
        self.help = 'Muestra una lista de los nombres de los macros guardados'

    async def handle(self, message, cmd):
        namelist = []
        for item in Meme.select().iterator():
            namelist.append(item.name)

        word = 'macros' if len(namelist) == 1 else 'macros'
        resp = 'Hay {} {}: {}'.format(len(namelist), word, ', '.join(namelist))
        await cmd.answer(resp)


class MacroSuperList(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self.name = '!list'
        self.help = 'Muestra una lista completa de los macros con sus valores'
        self.owner_only = True

    async def handle(self, message, cmd):
        memelist = []
        for item in Meme.select().iterator():
            memelist.append("- {}: {}".format(item.name, item.content))

        num_memes = len(memelist)
        if num_memes == 0:
            await cmd.answer('No hay macros disponibles')
            return

        word = 'macro' if num_memes == 1 else 'macros'
        resp = 'Hay {} {}:'.format(num_memes, word)
        await cmd.answer(resp)

        # Separar lista de memes en mensajes con menos de 2000 carácteres
        resp_list = ''
        for meme in memelist:
            if len('```{}\n{}```'.format(resp_list, meme)) > 2000:
                await cmd.answer('```{}```'.format(resp_list))
                resp_list = ''
            else:
                resp_list = '{}\n{}'.format(resp_list, meme)

        # Enviar lista restante
        if resp_list != '':
            await cmd.answer('```{}```'.format(resp_list))


class MacroUse(Command):
    def __init__(self, bot):
        super().__init__(bot)
        self.swhandler = ['! ', '¡']

    async def handle(self, message, cmd):
        # Actualizar el id de la última persona que usó el comando, omitiendo al mismo bot
        if self.bot.last_author is None or not cmd.own:
            self.bot.last_author = message.author.id

        meme_query = cmd.args[0] if message.content.startswith('! ') else message.content[1:].split(' ')[0]

        try:
            meme = Meme.get(Meme.name == meme_query)
            await cmd.answer(meme.content)
        except Meme.DoesNotExist:
            pass