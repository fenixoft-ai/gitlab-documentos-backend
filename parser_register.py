from flask_restx import reqparse

def parser_writer(fields):
    #usar matriz Nx3
    '''
        [nombre_campo, tipo_campo, texto_ayuda]
        .
        .
        .
    '''

    fields_length = len(fields)
    parserX = reqparse.RequestParser()

    for i in range (fields_length):

        parserX.add_argument(fields[i][0],type = fields[i][1], help = fields[i][2])


    return parserX

    '''parser_user = reqparse.RequestParser()
    parser_user.add_argument('email',type=str,help="the user email")
    parser_user.add_argument('password',type=str,help="the user password")
    parser_user.add_argument('name',type=str,help="the user name")
    parser_user.add_argument('picture',type=str,help="the user picture")'''