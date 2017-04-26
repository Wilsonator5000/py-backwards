from colorama import Fore, Style
from . import const


def _format_line(line, n, padding):
    return '  {dim}{n}{reset}: {line}'.format(dim=Style.DIM,
                                              n=str(n + 1).zfill(padding),
                                              line=line,
                                              reset=Style.RESET_ALL)


def _get_lines_with_highlighted_error(e):
    error_line = e.lineno - 1
    lines = e.code.split('\n')
    padding = len(str(len(lines)))

    from_line = error_line - const.SYNTAX_ERROR_OFFSET
    if from_line < 0:
        from_line = 0

    if from_line < error_line:
        for n in range(from_line, error_line):
            yield _format_line(lines[n], n, padding)

    yield '  {dim}{n}{reset}: {bright}{line}{reset}'.format(
        dim=Style.DIM,
        n=str(error_line + 1).zfill(padding),
        line=lines[error_line],
        reset=Style.RESET_ALL,
        bright=Style.BRIGHT)
    yield '  {padding}{bright}^{reset}'.format(
        padding=' ' * (padding + e.offset + 1),
        bright=Style.BRIGHT,
        reset=Style.RESET_ALL)

    to_line = error_line + const.SYNTAX_ERROR_OFFSET
    if to_line > len(lines):
        to_line = len(lines)
    for n in range(error_line + 1, to_line):
        yield _format_line(lines[n], n, padding)


def syntax_error(e):
    lines = _get_lines_with_highlighted_error(e)

    return ('{red}Syntax error in "{e.filename}", '
            'line {e.lineno}, pos {e.offset}:{reset}\n{lines}').format(
        red=Fore.RED,
        e=e,
        reset=Style.RESET_ALL,
        bright=Style.BRIGHT,
        lines='\n'.join(lines))


def transformation_error(e):
    return ('{red}Transformation error in "{e.filename}", '
            'transformer "{e.transformer.__name__}" '
            'failed with:{reset}\n{e.traceback}').format(
        red=Fore.RED,
        e=e,
        reset=Style.RESET_ALL)


def input_doesnt_exists(input_):
    return '{red}Input path "{path}" doesn\'t exists{reset}'.format(
        red=Fore.RED, path=input_, reset=Style.RESET_ALL)


def invalid_output(input_, output):
    return ('{red}Invalid output, when input "{input}" is a directory,'
            'output "{output}" should be a directory too{reset}').format(
        red=Fore.RED, input=input_, output=output, reset=Style.RESET_ALL)


def permission_error(output):
    return '{red}Permission denied to "{output}"{reset}'.format(
        red=Fore.RED, output=output, reset=Style.RESET_ALL)


def compilation_result(result):
    return ('{bright}Compilation succeed{reset}:\n'
            '  target: {bright}{target}{reset}\n'
            '  files: {bright}{files}{reset}\n'
            '  took: {bright}{time:.2f}{reset} seconds').format(
        bright=Style.BRIGHT,
        reset=Style.RESET_ALL,
        target='{}.{}'.format(*result.target),
        files=result.files,
        time=result.time)
