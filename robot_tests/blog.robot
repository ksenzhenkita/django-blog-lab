*** Settings ***
Documentation     Тестування додавання коментаря у блозі
Library           SeleniumLibrary

*** Variables ***
${SERVER}         http://127.0.0.1:8000
${BROWSER}        Chrome
${LOGIN_URL}      ${SERVER}/accounts/login/
${USERNAME}       admin
${PASSWORD}       Admin4life!
# Змінні-локатори
${BTN_SUBMIT}     xpath=//button[@type="submit"]

*** Test Cases ***
User Can Log In And Leave Comment
    [Documentation]    Перевірка, що користувач може залогінитись і залишити коментар
    # Ключові слова (Keywords) у дії:
    Open Browser    ${LOGIN_URL}    ${BROWSER}
    Maximize Browser Window

    # Логін
    Input Text      name=username    ${USERNAME}
    Input Text      name=password    ${PASSWORD}
    Click Button    ${BTN_SUBMIT}


    # Перехід на головну і відкриття першого поста
    Go To           ${SERVER}
    Click Link      xpath=//a[contains(@class, 'text-dark')]

    # Додавання коментаря
    Wait Until Element Is Visible    id=id_text
    Input Text      id=id_text       Тестовий коментар від Robot Framework!

    # клік через JavaScript, щоб обійти меню, яке перекриває кнопку
    Execute Javascript    document.querySelector('.btn-success').click()

    # Перевірка
    Wait Until Page Contains         Тестовий коментар від Robot Framework!

    [Teardown]    Close Browser