from commands.base.command import Command
import random


class Pat(Command):
    pats = [
        'https://media.giphy.com/media/68ikwD66c7UOY/giphy.gif',
        'https://media.giphy.com/media/r61gZfqvJZMtO/giphy.gif',
        'https://media.giphy.com/media/ZxnfBQHNHVgpG/giphy.gif',
        'https://media.giphy.com/media/TftK1iVPF1nC8/giphy.gif',
        'https://media.giphy.com/media/77XldNdVy4RLG/giphy.gif',
        'https://media.giphy.com/media/10KeKxHfeakzks/giphy.gif',
        'https://media.giphy.com/media/lZnEy2UefUZvq/giphy.gif',
        'https://media.giphy.com/media/ye7OTQgwmVuVy/giphy.gif',
        'https://media.giphy.com/media/SvQ7tWn8zeY2k/giphy.gif',
        'https://media.giphy.com/media/HxDOijFIr4g3S/giphy.gif',
        'https://media.giphy.com/media/vyDZlTdMzYJdm/giphy.gif',
        'https://media.giphy.com/media/109ltuoSQT212w/giphy.gif',
        'https://media.giphy.com/media/xVgGouGtc21H2/giphy.gif',
        'https://media.giphy.com/media/RputKS4rcCanm/giphy.gif',
        'https://media.giphy.com/media/iGZJRDVEM6iOc/giphy.gif',
        'https://media.giphy.com/media/ERUkEhOS1diV2/giphy.gif',
        'https://68.media.tumblr.com/f95f14437809dfec8057b2bd525e6b4a/tumblr_omvkl2SzeK1ql0375o1_500.gif',
        'http://33.media.tumblr.com/229ec0458891c4dcd847545c81e760a5/tumblr_mpfy232F4j1rxrpjzo1_r2_500.gif',
        'http://i.imgur.com/laEy6LU.gif',
        'http://pa1.narvii.com/6260/3fc8451fb1cba6fc5b0483b144d2507229a80305_hq.gif',
        'https://s-media-cache-ak0.pinimg.com/originals/c0/3f/58/c03f5817acde4b1c168d31ffe02c522e.gif',
        'https://media.tenor.com/images/2b2f9c5d046ea2cdaca41dfdc4356eea/tenor.gif',
        'https://38.media.tumblr.com/b4d110b98079b935512467aad091f068/tumblr_myki5bzz0U1shdfeho1_500.gif',
        'https://gifimage.net/wp-content/uploads/2017/07/head-pat-gif-13.gif',
        'https://media.giphy.com/media/e7xQm1dtF9Zni/giphy.gif',
        'https://68.media.tumblr.com/2d61aa2fd9286f5670fbb17b6e56475f/tumblr_o4ufimpBNt1tydz8to1_500.gif',
        'http://gifimage.net/wp-content/uploads/2017/07/head-pat-gif-16.gif',
        'http://pa1.narvii.com/6328/4f0d11f61890e80b83f9c7530f9e58ad60494c2b_hq.gif',
        'https://media.tenor.com/images/2280ed22d9f25bd2d15a7bbde188af1b/tenor.gif',
        'https://ugc.kn3.net/i/origin/http://giffiles.alphacoders.com/248/2482.gif',
        'https://68.media.tumblr.com/78996bab56fe7745b8727d8b334e465d/tumblr_omw4hjHzjP1skbmyho1_500.gif',
        'https://68.media.tumblr.com/3b72bb8d292b80c37f8a6d64d2ff0cca/tumblr_o9ha9ez6pv1v7p6apo2_400.gif',
        'http://i.imgur.com/L8voKd1.gif',
        'https://68.media.tumblr.com/584a3894e3483eed23d1afaf1f6f9347/tumblr_ok1oplyzSF1r0tp5lo1_500.gif',
        'https://media.giphy.com/media/2mwUG7WxQ25sk/giphy.gif',
        'http://i.imgur.com/tVIPzvi.gif',
        'http://gifimage.net/wp-content/uploads/2017/07/head-pat-gif-11.gif',
        'http://i0.kym-cdn.com/photos/images/original/000/915/038/7e9.gif',
        'https://media.giphy.com/media/13YzqRtgyD4dOw/giphy.gif',
        'https://33.media.tumblr.com/cb4da84b16d8e189c5b7a61632a54953/tumblr_nrcwmt2SNG1r4vymlo1_400.gif'
    ]

    self_pats = [
        'https://media.giphy.com/media/wUArrd4mE3pyU/giphy.gif',
        'https://i.imgur.com/fWQ6dqe.gif',
        'http://pa1.narvii.com/6401/655b40f33530a90101682ee74c5fa12a673df749_hq.gif'
    ]

    bot_pat = 'http://i.imgur.com/tVzapCY.gif'

    def __init__(self, bot):
        super().__init__(bot)
        self.name = 'pat'
        self.help = 'Te envía una imagen de animé de una caricia en la cabeza y algo más'

    async def handle(self, message, cmd):
        if len(cmd.args) != 1 or len(message.mentions) != 1:
            await cmd.answer('Formato: !pat <@mención>')
            return

        mention = message.mentions[0]
        text = '{}, {} te ha dado una palmadita :3'.format(
            Command.final_name(mention), cmd.author_name
        )

        if mention.id == cmd.author.id:
            url = random.choice(Pat.self_pats)
        elif mention.id == self.bot.user.id:
            url = Pat.bot_pat
            text = 'oye nuuuu >_<'
        else:
            url = random.choice(Pat.pats)

        await cmd.answer(embed=Command.img_embed(url, text))
