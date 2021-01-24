import logging
from user_model import IQUser
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from iqoptionapi.stable_api import IQ_Option

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

EMAIL, PASSWORD = range(2)

def login(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Insira seu email da conta IQOption:')
    return EMAIL


def email(update: Update, context: CallbackContext) -> int:
    context.user_data['email_iq'] = update.message.text
    update.message.reply_text('Insira a sua senha da IQOption')

    return PASSWORD
'''
def password(update: Update, context: CallbackContext) -> int:
    context.user_data['password_iq'] = update.message.text
    print(context.user_data['email_iq'], context.user_data['password_iq'])
    try:
        context.user_data['iq_object'].close()
        del context.user_data['iq_object']
        print('del na iq')
    except:
        print('nao deletou iq(nao existe)')
    iq = IQUser(context.user_data['email_iq'], context.user_data['password_iq'])
    print(iq)
    print(iq.login_success)
    context.user_data['iq_object'] = iq
    del context.user_data['email_iq'], context.user_data['password_iq']
    context.user_data['logged_in'] = context.user_data['iq_object'].login_success
    print(f'login_success:{context.user_data["logged_in"]}')

    if context.user_data['logged_in']:
        update.message.reply_text('Logado com sucesso!')
        return ConversationHandler.END

    update.message.reply_text('Conta inválida. Insira o e-mail novamente:')
    return EMAIL
'''
def password(update: Update, context: CallbackContext) -> int:
    context.user_data['password_iq'] = update.message.text
    email, password = context.user_data['email_iq'], context.user_data['password_iq']
    print(email, password, sep=' - ')
    api = IQ_Option(email, password)
    api.connect()
    check = api.check_connect()
    print(check)
    if check:
        update.message.reply_text('Logado com sucesso!')
        return ConversationHandler.END

    update.message.reply_text('Conta inválida. Insira o e-mail novamente:')
    return EMAIL

def status(update, context):
    pass

def start__(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'I see! Please send me a photo of yourself, '
        'so I know what you look like, or send /skip if you don\'t want to.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Gorgeous! Now, send me your location please, ' 'or send /skip if you don\'t want to.'
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, ' 'or send /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Maybe I can visit you sometime! ' 'At last, tell me something about yourself.'
    )

    return BIO


def skip_location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'You seem a bit paranoid! ' 'At last, tell me something about yourself.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel_login(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Cancelando login', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1573816931:AAE-xaEZJxmnAd0Akv009u5Ky3Nj-qSlZjM", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    # conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('start', start)],
    #     states={
    #         GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
    #         PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
    #         LOCATION: [
    #             MessageHandler(Filters.location, location),
    #             CommandHandler('skip', skip_location),
    #         ],
    #         BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    #     },
    #     fallbacks=[CommandHandler('cancel', cancel)],
    # )

    login_handler = ConversationHandler(
        entry_points=[CommandHandler('login', login)],
        states={
            EMAIL: [MessageHandler(Filters.regex('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'), email)],
            PASSWORD: [MessageHandler(Filters.text & ~Filters.command, password)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', skip_location),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel_login)],
    )

    status_handler = CommandHandler('status', status)

    dispatcher.add_handler(login_handler)
    dispatcher.add_handler(status_handler)
    # dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
