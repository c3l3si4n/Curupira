from ..database.setup import Attempt, Challenge, User
import utils.logging.log as log
from datetime import datetime
import discord
import peewee


def check_flag(ctx, challId, flag, discordId):
    """
    Essa funcao verifica se a flag esta correta, criando sempre um Attempt

    @Params
    :challId => ID da Challenge
    :flag => flag do Challenge
    :userId => ID do Usuario
    """
    user = User.get_or_none(User.discordId == ctx.author.id)
    if user is None:
        return discord.Embed(title="Regitre-se", description="Use $register para se registrar")
    else:
        try:
            chall = Challenge.get_by_id(challId)
        except Exception as e:
            log.err(e)
            return discord.Embed(title="Chall?!", description="Esse challenge id não existe!")

        try:
            Attempt.get(Attempt.correct == True, Attempt.user_id == user.id, Attempt.chall_id == challId)
            return discord.Embed(title="Chall?!", description="Você já submeteu a flag desse desafio!")
        except peewee.DoesNotExist as e:
            log.err(e)

        if chall.flag == flag:
            try:
                Attempt.create(user_id=user.id, chall_id=challId, flag=flag, correct=True, timestamp=datetime.timestamp(datetime.now()))
                User.update(score=user.score + chall.points, last_submit=datetime.timestamp(datetime.now())).where(User.discordId == discordId).execute()
                return discord.Embed(title="Chall?!", description="Parabéns! Flag correta!")
            except Exception as e:
                log.err(e)
                return discord.Embed(title="Chall?!", description="Erro ao criar Attempt True")
        else:
            try:
                Attempt.create(user_id=user.id, chall_id=challId, flag=flag, correct=False, timestamp=datetime.timestamp(datetime.now()))
                return discord.Embed(title="Chall?!", description="Flag incorreta!")
            except Exception as e:
                log.err(e)
                return discord.Embed(title="Chall?!", description="Erro ao criar Attempt False")
