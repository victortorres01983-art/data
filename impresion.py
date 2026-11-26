import win32print
from datetime import datetime


def imprimir_ticket(codigo, opcion):

    impresora = win32print.GetDefaultPrinter()

    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")

    ticket = (
        "\x1b@"                  # Inicializar impresora
        "\x1ba\x01"              # Centrar texto
        "\x1bE\x01"              # Negrita
        "CENTRO MEDICO\n"
        "\x1bE\x00"
        "Terminal de autogestion\n"
        "--------------------------------\n"
        "NUMERO DE ATENCION\n\n"
        "\x1d!\x11"              # Texto grande
        f"{codigo}\n\n"
        "\x1d!\x00"              # Texto normal
        f"{opcion}\n"
        "--------------------------------\n"
        f"Fecha: {fecha}\n"
        f"Hora: {hora}\n\n"
        "Aguarde a ser llamado\n"
        "Gracias por su visita\n\n\n"
        "\x1dV\x00"              # Cortar papel
    )

    h = win32print.OpenPrinter(impresora)

    try:
        win32print.StartDocPrinter(
            h, 1, ("Ticket Medico", None, "RAW")
        )

        try:
            win32print.StartPagePrinter(h)
            win32print.WritePrinter(
                h, ticket.encode("cp850")
            )
            win32print.EndPagePrinter(h)
        finally:
            win32print.EndDocPrinter(h)
    finally:
        win32print.ClosePrinter(h)