from pysignalclirestapi import SignalCliRestApi, SignalCliRestApiHTTPBasicAuth
from getpass import getpass
import os, json, inspect, argparse, urllib3
urllib3.disable_warnings()

callable_methods = [x[0] for x in inspect.getmembers(SignalCliRestApi, predicate=inspect.isfunction) if x[0][0] != '_']

parser = argparse.ArgumentParser(description='Comandline wrapper for SignalCliRestApi')
parser.add_argument('--number', help='Your phone number, e.g.: +4917612345678', type=str, nargs=1, required=False)
parser.add_argument('--url', help='URL to Signal-CLI-REST-API Server, e.g.: http://localhost:8080', type=str, nargs=1, required=False)
parser.add_argument('--auth_user', help='HTTP-Basic-Auth User', type=str, nargs=1, required=False)
parser.add_argument('--auth_password', help='HTTP-Basic-Auth Password', type=str, nargs=1, required=False)
parser.add_argument('--json', help='Return result as json', required=False, action='store_true')
parser.add_argument('--settings_path', help='Load settings from custom path', type=str, nargs=1, required=False)
parser.add_argument('--store_settings', help='Store the values of: number, url, auth_user, auth_password, skip_ssl_verification in a settings file, the default location is ~/.config, if you need to use any other path be sure to hand it over with: --settings_path  or set a enviromentvariable: SCRAC_SETTINGS="/..."', required=False)
parser.add_argument('--verify_ssl', help='Skips the verifications of SSL Certificates (Use for self-signed certificates)', type=str, required=False, default="True")
parser.add_argument('command', help='[ ' + ' | '.join(callable_methods) + ' ] type "command help", to get futher information on this command', type=str, nargs='*')
args = vars(parser.parse_args())

if not args['settings_path']:
    if 'SCRAC_SETTINGS' in os.environ:
        args['settings_path'] = os.environ['SCRAC_SETTINGS']
    else:
        args['settings_path'] = os.path.join(os.environ['HOME'], '.config')
else:
    args['settings_path'] = args['settings_path'][0]

settings_file = os.path.join(args['settings_path'], 'signal-cli-rest-api-client-settings.json')
if os.path.isfile(settings_file):
    with open(settings_file) as json_file:
        settings = json.load(json_file)        
    args.update(settings)

if not args['number'] or not args['url']:
    print('No Number and/or URL where found. Please check settings and/or settings path.')
    parser.print_help()
    
    exit(1)
elif isinstance(args['number'], list):
    args['number'] = args['number'][0]
elif isinstance(args['url'], list):
    args['url'] = args['url'][0]

authentication = None
if args['auth_user']:
    if isinstance(args['auth_user'], list):
        args['auth_user'] = args['auth_user'][0]
    if not args['auth_password']:
        args['auth_password']=getpass(prompt='HTTP BASIC AUTH Password: ')
    elif isinstance(args['auth_password'], list):
        args['auth_password'] = args['auth_password'][0]
    authentication = SignalCliRestApiHTTPBasicAuth(
        args['auth_user'],
        args['auth_password']
    )

if isinstance(args['verify_ssl'], list):
    if args['verify_ssl'][0].lower() in ['false', '0', 'n', 'no']:
        args['verify_ssl'] = False
    else:
        args['verify_ssl'] = True

if args['store_settings']:
    del args['command']
    del args['settings_path']
    with open(settings_file, 'w') as f:
        json.dump(args, f)
    if not args['command']:
        exit(0)

if not args['command']:
    print('No command, please enter a command.')
    parser.print_help()
    exit(1)

if args['command'][0] in callable_methods:
    signalclirestapi = SignalCliRestApi(args['url'],
                                    args['number'], 
                                    auth=authentication,
                                    verify_ssl=args['verify_ssl'])
    if len(args['command']) == 2 and args['command'][1] == 'help':
        print(inspect.getdoc(getattr(signalclirestapi, args['command'][0])))
    else:
        sig = inspect.signature(getattr(signalclirestapi, args['command'][0]))
        parameters_min = []
        parameters_max = []
        for param in sig.parameters.values():
            if (param.kind == param.POSITIONAL_OR_KEYWORD):
                parameters_max.append(param)
                if param.default is param.empty:
                    parameters_min.append(param)

        if not len(parameters_min) <= len(args['command'][1:]) <= len(parameters_max):
            print('Wrong number of arguments for command')
            print('Expected: ' + ' '.join(parameters_max))
            parser.print_help()
            exit(1)
        if len(args['command']) > 1:
            result = getattr(signalclirestapi, args['command'][0])(args['command'][1:])
        else:
            result = getattr(signalclirestapi, args['command'][0])()
        if result:
            if args['json']:
                print(json.dumps(result))
            else:
                print(result)
else:
    print('Command not found!')
    parser.print_help()
    exit(1)
exit(0)
