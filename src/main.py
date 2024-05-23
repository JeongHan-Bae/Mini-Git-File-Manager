import os
import pickle
import sys
import base64
from typing import Optional, List, Tuple

# Set the path of the Git executable
os.environ['GIT_PYTHON_REFRESH'] = 'quiet'
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = 'C:\\Git\\bin\\git.exe'

# Now import the Git Python module
from git import Repo

from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QApplication,
    QFileDialog,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QPlainTextEdit,
    QListWidget,
    QMessageBox,
    QWidget,
    QGridLayout,
)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QCoreApplication

import hashlib
import datetime



def get_absolute_path() -> str:
    """
    Retrieves the absolute path of the current script's directory.

    Returns:
        str: The absolute path of the script's directory.
    """
    exe_path = os.path.abspath(sys.argv[0])
    return os.path.dirname(exe_path)


# Global variables
formats: Optional[List[str]] = []
# Check if the directory exists, create it if necessary
path: str = os.path.join(get_absolute_path(), "..")
if not os.path.exists(path):
    os.makedirs(path)

# The General Font Most used
GENERAL_FONT = QFont("Monospace")
GENERAL_FONT.setStyleHint(QFont.TypeWriter)
GENERAL_FONT.setBold(True)
GENERAL_FONT.setPointSize(10)  # Set font size to 10


# Util Funcs
def get_icon() -> QIcon:
    """
    Retrieves an icon from an image file.

    Returns:
        QIcon: The icon loaded from the image file.
    """
    encoded_string = (
        "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"
        "OzhuOSrAsSwLM2Dxl+mv0Kh5gFkvPI50RdTmBdJ2"
        "EYbHHaOHVLCOchvufvBDBnZJISIcgp6tVdRzTT75"
        "4CNWL1vNyJkTlI5g257GENMIYgYFCW4cs5/8PcVL"
        "h2u0t+0QhnsM97DAFSZxXoRCmnLG+PdYnJdVYbq1"
        "CkBtRIWzM+b8QFCp0782Nv3u9oRcdbKV4bKySf9z"
        "1avS1SjVHp6m3JLy/wZ/fuspUF5Fqud8dR951+W+"
        "qSiv4RiMfuADBnduiDBNHfg4uDwwahaOjGAZDvPz"
        "tp1gBmqeBOkwoHU/ipcPp7RxX5LO6YWz+x3KDjUj"
        "ue8tFP39GRyCnDXmnyzO26jn1kuX1YhQ9XDYFQbX"
        "pPZkdX4mRYYCKKFVToGrBn4MVmT/TLvUOFq1TmLN"
        "lgIu79kMtwp7G5aWTsvzWjFlyjSmjZumXdMf3noe"
        "4YYxFBJGnZICgoh6zrC11whZDRh/533612F3juP7"
        "b75h55ZlzM/LqYq7ftoMiJMel7Xqw/ENV+OlP4Jh"
        "l1G++3Xytoc4+8Z7KJ07nRK3CR3Gv8enB7bUrQFa"
        "nTG4Nq1n1KIFhiE00xox4U5ue+BeLcUN2w7RKjVE"
        "q9Rk1m79iQHdmuApYNMCFlyT1ou0Dq24b9q9xAVM"
        "AqYCtwejAKUkaWoeIRVTqbh8Cnz9pAeIOFInVfbl"
        "bGTHluUszN1eqwASpeSXbXpz+LUBlBOg0cinCL/3"
        "MHsDbTjzpnuRbz9CiWxO+3Fz+fRAVRMAlRmuyAn6"
        "qWpfJdUGf/frx3nhuQcIxEUwvXLKyuK4uMdlFAUi"
        "rM79Wtt0bZfPIyTDlAClgTQ8hOfx4lsv4DqKpCqc"
        "MjlSIsg7WkrewbBOYEhDIFTuUGe9bD6Z8wohR8GZ"
        "ixBhFuRv05qn6I3AQRqWxquQ63FZu978/PJlGiPU"
        "BEqomvgINMgek61pN/YvGgOUy1ZXDQzws8JqIUq1"
        "3nv2FbxSm/35R3DDDi+/9BjSO6qWQr8ug3hp/l/1"
        "yK7n6fDX9VxKS20u+EWvmGYyPDWd+JYt6N6tDxs+"
        "+1znAjFcXnrrj1pAh4oi/HykjP0/FWJaSmiG5g/v"
        "vzRbU1lXwEXDbuBwwUH2ZCkT2KYp7+qsQ3hmQCdT"
        "B/VogoNHvCcY3LoPyi9LJcEY0ldsVrDo0HqkY9Tu"
        "BmPBkNIAG1fbv6ddmYHlCbbuyiBsFyKF4IN1x/nt"
        "2FtxjbAvSZWUlBLhWQRNyaK9m4kEBMPTuhFq0oiJ"
        "U+6jU/vW+p47b5mg/bQiKv7lL1ZncfTJ+qdz3X2z"
        "cLxizTN2b97Id9nLWZDna4BQglT/12zSD7KkYeDg"
        "MKJFX8riBf9cuQI9iYSQFNzQrz+LCrZoN+yfvj/3"
        "CQkRpQG2UIyvO1t3rtanohBBqZPtlfKPlcV4XoRr"
        "Lj+L7u0b+pNLiSsk8z7KZtRNY1j+42ZKAibXpHTV"
        "Apjy4GTOa5uqsf/I0eNs+Kocx7D9sfXGVSI5KgTl"
        "JTSZidYCPMHuLRv4NmsVi/KqkpiaxudLdHhqN8Jm"
        "mHJbeQyhuBfLMsPc0L8/iw7k+C5b8RatISdJitqu"
        "y+Vt+zDtuTe0PSpVs4yA9t069aXDcEVElI1ZGG6E"
        "kJR0SjvGqJsnsSx3A8etANemdifQOImpD97H+e1a"
        "avUtKj7u+xDlVTwX25YaYF0zSM53RT76CMGxsrDG"
        "IeUt9mxZxzeZq1iUf6IAaqbmr01Np4QwtrtDbzbO"
        "Op+AaIglbOYX5OiUfUXNsjoVrnSDWh1Nk6tb9ND2"
        "5MsqChyKjKlvouA2+Y/vYBChW2opwpTcPmIyK/Zv"
        "0hpwbUoPAk0SmfbgfZxzVksNcoWFx7hr9BVa8SuC"
        "qSh/1Log4VeT/4GtAVaBIuzJ2sC3W6oLoOb5X3fR"
        "QEp//JmgHdR03uEYQZrTvV8qy1d8QsPQ+biGydK8"
        "L/0ahE6a1DABRTljlyo8XJPWgwU5myksDWOogMQw"
        "uPeWkRTnfcc/9m2igRNgYOtuWkgKfdXJLf5mDW5y"
        "ENcwuLpFd+KaJDLlwUmc21aFyQaFRYcZPWZIRbZH"
        "ofXFTx1ixYwUzQGU8G+9931EKIDj2YqV8X3WRr6p"
        "IYBYhUjXCaTNVandcXQBQvF5pa3KV4Rpf25Ttu1Y"
        "rrGkSWIXpBNgfv5mjWU1iJDKCFURgNpASncKIzkY"
        "ph+6Kh04/+yrKMg7xKf7s7SsGigy4puyNpdj0RBX"
        "DT68ZRfikxO5/7FpdGibqrXo2usvqnZ4atz+s3Yh"
        "SWDpY61ItHwTu/m+j3GEjeG6fL9xLbtyVrMgv3Ye"
        "0MiAS1qqMHhTND6vylD96E87RmnRyEpn4U+ZOklS"
        "azQYKygoVB2e0p1Ddg4hlVSRsGnbEe4Z8zBff/kV"
        "AbuMZfk5RKK8oWq2JVbiGt6yK6HGSUx7eCpntmnG"
        "zTdeXLF56R2j9xNH2DCrNfsiJnc8/SMizmXhg61p"
        "aPl5gBET3wfpsWfTWnZvzfC9QGxvygRVWsaDpIDg"
        "0pQevLN6LVKHatHiasXafE+lXPZdv7yMRQe26IKL"
        "SphUywnGUmJqEkVXrkntwdpvN3LMMbR9v/nGR8yd"
        "/SJClDNi+BUs/ngl6cN6M2POH6Kkw6/GxAQwLK0r"
        "8U0aMOWhybRt05ybbvIF4MkSej9xmLdnnMkFlktR"
        "NL4b9kQuHz7RmhZRMd0w4QPt8vZsWcuerRnMz42C"
        "oDRYlbUXz2isCyc39GzExc178O661ThaizXR115G"
        "kyapijjKsxiMuqQ/iw/k6LDk5AIwDPbk7GDiFbdz"
        "2/3TiSAIWCbv/v4Z4r1yQglJZGR/SO/zhyhzY9GP"
        "2dUKEVUFENckifsfmEz7M1pw482X6K1d8uhmvEAK"
        "lhNWK2Pl8+01b+n/7I+snn5GRTShBOBJm71b1rNn"
        "62rm50Y1QAlZMUbFPwxDM73181fyzNhpOhusSxR6"
        "8/D8O2+S0r4tW1etZvb0J7hryRKu6do0mpypRQOU"
        "CeiSV2ovNmxfSP8LryQSUa5Omw07dq3BoZj/WXKY"
        "308ciTQ93t65kWZJfgxQoX7KJ7fsRqhxIhOnTaJj"
        "25bccGP/6A0R+j2QhZGcwtLH0vhur0vHdkmUCUhy"
        "JMLyB7r+3o+QlPPjlg18l7NKM8Fa+wCkQASUz3e4"
        "NrUfs99/i2bt2nFD+kUETBX9q7yTZNKSDIZ0jceO"
        "5gZPigG24XB9Sm/WbVsIoXid/QsFTQ0if/9sN7Zt"
        "kd6unJuHjUOGQkyd/yGDu6VVaIHmwsLj6rReBBvF"
        "M2HqZDqd3QYpwtwwwjcDKctxPYPLZ2TT/owG7Mi1"
        "WPX0OVgx9R/3V2RcHKbrahPYlbWKhVVAMNZio25X"
        "nELlMK9M6430LEq8jSqoZ+lXNkO79SVRuty7aBlX"
        "pTfBUXk9nXesEQ6r2qDvehUTlFyf1ouBA4fTe8gw"
        "yk0LAg0w3ENMH9eT5qGLUGTJ9SRGSLJgX2a1QfUH"
        "4TEktReJTROZMHkSnc5J05N27nI253RQVq7K6B7D"
        "H82kKJSibXb22LPomWaz5ZtCfvfKKp0TUNeeTRns"
        "ys5gsQqGaqQghGkwYcjt7N28UxMnRdZw/U0aKsBS"
        "QCkcRn++nOFdmlWrGFXTAL8/IEoQVBrL9Bie2pc3"
        "5r3HroPFfPjqs2zPmacHdm1oFNeTL/IyCdsuyk2E"
        "MVi/7RCmdIgPeqSf35xhrfoS16QhEyePo9M5MSJU"
        "yqi7Lot2iljaQd30m2x+e38Pzgwp0u1x59SPsB0H"
        "VSFSQPXdxjV8l7OWqYuWMKhbC90cERNE8Gg5gzv2"
        "oTiy3Y8Qo6lwpfLJZi8dWzRo24L3183HEzH9ijmj"
        "E4iQxujorwYRGeG6Vv00YBi6AJEde5LG8d0pDTus"
        "OrCNiE7JCb7ec1gjb2ICfPVzgDkDLyEhpSF3Txgf"
        "1QCTI4XH2V/oMvOBKyuSK1Hg0J0ed97/gY5UHMep"
        "AKrdG9ewO3sdE5eswpUBBvdI0JikhJBQ7DHgvN6U"
        "2JmMei5Dzx9xDeY+dBEJwW7EmSEW5G5AhU818aM6"
        "Bjw3xtfcGo2O+nPQYEjj7ohAhOLIDl8LOEoDcRnS"
        "KGdN7nZKLMXblSCkdomf7SzhjQG/ICzVCGW89taf"
        "VYSOpwiFiukNQwviYGHUbyvlVM97HkePH/cbtoRg"
        "wWsvYrilGMJiwpIv8FyDK7snIKWlNxQ6EmFwp19Q"
        "WLaeyW9+RcBU0aLkD6M7kRC4EKuJycId63X+QUWh"
        "1bN49aoOG7rFZeg5/XCPlFEUyWbzruOUS1NHm0PP"
        "vwRhOriGx9IDWbieIhyw9OsS3SXy6qArsHGwDIUZ"
        "gjsefBLHdXAdl3J1iq7jJ0ulwDBVsKVcm8WnL/+W"
        "eM/AVU/HJTFp/idaY67slIBnhIiXkr5ndiY+EtJH"
        "VuJm+2w0ihHq72SrV6zrSCdlFqqEaDQG8DW9DgEo"
        "CSv6elVqN775fiuRMo/undIpNxxCTkAnRDbvWMrW"
        "rF0U5B9k5iOzWJCXhVSoLG1WZudSbDQm6x9/Y/Pc"
        "d3W2R5mSOt5b75lKqQp9pUpg+CF1yJB8/PKfcQ2J"
        "7QU1iCV27Mwdf/wDyRQxoEsrhAho8Ly6ZW9sHVFF"
        "/GKLH6JFKZCffA16CdoFfj+7Px3uX8rCgyofECVJ"
        "J8sHVO2wUgtTk1yXls6TL79GYjDMgP7nkn7uFVw8"
        "sDd/ev1xbJFCVtYumibAiKG38nlepqaZSnRqUwtz"
        "DmMJSxcpVawx+/LLNLrHeokqddLx6arSLBzuW7Qe"
        "z4josoNnuQzp1LgCf9R9V6ZdyKJ3fsXF3ZVAKyvP"
        "OmbRaiBJ7jaXgldvxfLySLkng/kHN0UbwWLV4nqY"
        "QNiE69PSeXT2uziewLELad+2OWVOhLxDQb2Zc5p5"
        "nNUsyFWDfsWigo0q5I5mbHVEX7HwmNpV+SL6Zyyd"
        "Xh2E9f1RThF7xjUFN7T8BRGvnE/euI0BF6qKIwRL"
        "E/zNlcfjNf1Zh97JXebqalZS+XEe2bCW+QWZ+p7K"
        "3oEalSG/TlW9QcKVkuGt03ls9jt4bikd0kx2HorH"
        "CBjE/avyMmPUHQRUPUvHAA6LC7JwAgbXN+2tM/sx"
        "t61Ab17+5sq0epSIxDhDzcbp2jo8B53RlSQvRLkj"
        "MU2Tj16/noG9TfKfjZCU5HI0vojgscYUNDtI51+3"
        "pXHnufzw6mSSI9k0nbye+QWbELEKcX1MwGc3Bmvm"
        "L+OFux9C6qP163mjH5jB2endSJDHGHXj+XTsMIDc"
        "70t1bU4hbrO0hiz54mOfq0uTruf/QvuOhQd80qSj"
        "R+FxRaueBL0Aiw9s1BFnLI6ImaLOEVoOg5p3JUAD"
        "xk+6mt/9cRrJgT589PqN/LKPSekTNnEdigje3grx"
        "vSRv2V7SxqfRqOPfyH3tdkJuAU0nZLDw4CZVWdNa"
        "qbvYa4sGa+3YVtHX0h8wTJuwtHnp9js4JuC1RYuJ"
        "DyQQJw9y7YAz9bCKiu7aU6Dj52f+sl6nw4XnYlge"
        "82b/loUF2RWESzHFoAhRzlFCJLIobwO2Idi+L8L7"
        "n+fz3N1naPxxMPHMMEeO5+jUnLLzpOCFLJxzI5f2"
        "UeTG5Ogztta20kAZqVMSkQGbBp3/Ru6fbyXEYZpN"
        "XM6iA5naPHUm72TV4draTJWkdu4v1n58f7HBvMdn"
        "cnhjhg49XRlh7hcrEIkJWK7JOU2KojYm+P2cDN5/"
        "8XmtFYqdGp5g6YFNjL/6TsrCpRRszWXXhidJjf9W"
        "A1brHh206zxWnszUF37DrGHDiXhllNg7sKI4F5Fh"
        "1mz3uD69H0v+OpJe3SIaR1XPgaE8Six5J2waXvA/"
        "HH5pGMFQCQ3GrWRBXrafhK3oIa4HCFYClp/2Wb39"
        "R0pEIyxT9etK/njFUOLs4wjDpNwwuGXi4zw4ursK"
        "oHnxz+/z1pw3sYjDcW2W78tk8Hk9CCmq7Sjf7/Ht"
        "xqdIiy+gaddXNfVV5lBqBCl2VECj0mz+ClRYvG6r"
        "jW1Khva5BBH2yPjdbXRoWKhzeyplpxK0urAjJYaw"
        "SRu7RBdlVfve+C+Wc1XnJr5VV4laa22SOlWXqPLx"
        "6jKlR1gVPgXEBWDfpm8YP+wWRkyZSdtWbXGN4zpb"
        "Y1nQrl0am3eU8c5DIymWEVp4xez98n4sUYJHkl8N"
        "cgOU5+zFjk8i7bZ5HHcr+wH2H3bZmQ/3jLiG/N37"
        "dK2/y+ABfL10g1+dUt2kwi/X+rotUDGR0gsz6DD/"
        "R2V2Sph+TeCkGhArjdX1Ho4iHf1amKz7qZI6K9tK"
        "kILBbXoxd97vOE5zduZJ+pwlWbXtCCIQx6sP3c3H"
        "B7K4IbUXTZMOsSNjKnFdVQ+xyrMfx/7b0zQZvZTi"
        "yCa/qKHJjUnWtzCoUzeEK1m+dyulCYpAKdrsonoW"
        "Y39raFUpfGH57xgAlmcSUY2T0VOv+qZKnUywpr/2"
        "GRs40tAasDS7mLPTLM5plaBtzw3AlyuyeOzG8dFE"
        "pO4A0moZkBalDSSrv81kSEp/WjTKJ2f9/cSfN94H"
        "pXAR4X88R7ORi3lnzUpMN6AJzZX9GuMVQdqZPZn3"
        "/ZYqVWXf7dsSMrIK9VIH9WgcxYPKldd8Z6mau63m"
        "BWoEQ7VlXqoKRJmCSpWtz8n1U+Ja+hYX9W5KIKLC"
        "VVVKF7oUpQ5TOGAHJUPb9CVku+x8ty+JToLO2KiT"
        "jWDpULo0KUSbmz9HvXugqa1QPWomH+dm6nTn+q0F"
        "0U4RVa+QRFyHS3u2xDX8Mnks0VGTX9SaSaqPACrL"
        "SDX1wf+8O78I6aquL3SR9LsCh7hgADNgEy5TlFMl"
        "Uwwu6aS0ROrSFULlmJRumOx/+1aC7s+kjP68YgLV"
        "6DjvUKYutasTyz8U4Zv9pbqtvnVjiRVQkZ1uc0AI"
        "i/at4mtd3MmwrFIYp+oTjDI133Tq9wqKIxzW5KgO"
        "Qf9SnR4DL4hnb5HNdz+GdaOUZ5pIVaUwDH5/+UDy"
        "3x6H6RwhbdT7TFq2goALtiUI2H6ApEFLp7wkgzsl"
        "6opVXVft9l751Em9wMk6RU/lFWLD6nuUe9P016qI"
        "S7UNKrekKJi0KBMGxwVs/rIQ1zR4bdAVqrWaCctW"
        "YDqCsBBc1rERcYS1qjsqiyNUu4bqTK3fQdRnvVqw"
        "MROIvTZ3KgHUlHpNT1HvSVUIrDRBldNU6VpRUwFl"
        "SmOiBZhgFa2rDYjr8lJ1aUjl79HX5tQX/40XJ+s/"
        "cd131legdY/k31HbeBUvTqob/tNXZ//bCz7Vxv4b"
        "c53w6mxVIYx9fnQt80fbS/+tN0Dqez7/wX2nIY05"
        "D7154svTVZfw/+31+f8FzikB3CWeBcwAAAAASUVO"
        "RK5CYIIA"
    )

    # Decode the base64 string to binary data
    image_data = base64.b64decode(encoded_string)

    # Convert binary data to a QPixmap
    image = QPixmap()
    image.loadFromData(image_data)

    # Create a QIcon from QPixmap
    return QIcon(image)


def _path_formatted(_path: str) -> str:
    """
    Formats the provided path for better readability.

    Args:
        _path (str): The path to be formatted.

    Returns:
        str: The formatted path.
    """
    return "\n".join([_path[i: i + 40] for i in range(0, len(path), 40)])


def recover_formats_from_gitignore(repo_path: str) -> None:
    """
    Recovers formats from .gitignore file located in the repository path.
    Sets the global variable 'formats' with the recovered formats.

    Args:
        repo_path (str): The path to the repository.
    """
    global formats
    formats = None
    gitignore_path: str = os.path.join(repo_path, ".gitignore")
    with open(gitignore_path, "r") as f:
        lines: List[str] = f.readlines()
        # Filter out lines starting with '!' and '*'
        formats = [line.strip()[1:] for line in lines if line.startswith("!")]


class MainWindow(QMainWindow):
    """
    Main window of the application.
    """

    def __init__(self):
        super().__init__()

        self.setWindowIcon(get_icon())
        self.setWindowTitle("Git File Manager")
        self.setGeometry(100, 100, 600, 400)  # Set smaller window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_layout.setAlignment(Qt.AlignCenter)  # Center-align the layout
        self.central_widget.setLayout(self.central_layout)

        # Set background color to transparent
        palette = self.central_widget.palette()
        palette.setColor(self.central_widget.backgroundRole(), QColor(10, 16, 24))
        self.central_widget.setAutoFillBackground(True)
        self.central_widget.setPalette(palette)

        self.setWindowOpacity(0.6875)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        # Set font
        label_font: QFont = QFont("Monospace")
        label_font.setStyleHint(QFont.TypeWriter)
        label_font.setPointSize(12)  # Set font size to 12

        self.repo_path_label = QLabel("Repository Path:", self)
        self.repo_path_label.setAlignment(Qt.AlignCenter)  # Center-align the label
        self.repo_path_label.setStyleSheet(
            "color: rgb(227, 239, 255); font: bold"
        )  # Set label style
        self.repo_path_label.setFont(label_font)  # Apply thinner font

        self.repo_path_value = QLabel(path, self)
        self.repo_path_value.setAlignment(Qt.AlignCenter)  # Center-align the value
        self.repo_path_value.setStyleSheet(
            "color: rgb(227, 239, 255); text-decoration: underline"
        )  # Set value style
        self.repo_path_value.setFont(label_font)  # Apply thicker font

        self.check_commits_button = QPushButton("Check Commits", self)
        self.check_commits_button.clicked.connect(self.check_commits)

        self.change_path_button = QPushButton("Change Path", self)
        self.change_path_button.clicked.connect(self.change_path)

        self.commit_current_button = QPushButton("Commit Current", self)
        self.commit_current_button.clicked.connect(self.commit_current)

        self.change_formats_button = QPushButton("Change File Formats", self)
        self.change_formats_button.clicked.connect(self.change_formats)

        self.check_commits_button.setStyleSheet(
            "background-color: rgb(20, 32, 48); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, "
            "12); border-radius: 3px; padding: 5px;"
        )
        self.change_path_button.setStyleSheet(
            "background-color: rgb(20, 32, 48); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, "
            "12); border-radius: 3px; padding: 5px;"
        )
        self.commit_current_button.setStyleSheet(
            "background-color: rgb(20, 32, 48); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, "
            "12); border-radius: 3px; padding: 5px;"
        )
        self.change_formats_button.setStyleSheet(
            "background-color: rgb(20, 32, 48); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, "
            "12); border-radius: 3px; padding: 5px;"
        )

        self.check_commits_button.setFont(GENERAL_FONT)
        self.change_path_button.setFont(GENERAL_FONT)
        self.commit_current_button.setFont(GENERAL_FONT)
        self.change_formats_button.setFont(GENERAL_FONT)

        button_layout = QGridLayout()  # Create a grid layout for the buttons
        button_layout.addWidget(self.check_commits_button, 0, 0)
        button_layout.addWidget(self.change_path_button, 0, 1)
        button_layout.addWidget(self.commit_current_button, 1, 0)
        button_layout.addWidget(self.change_formats_button, 1, 1)

        self.central_layout.addWidget(self.repo_path_label)
        self.central_layout.addWidget(self.repo_path_value)
        self.central_layout.addLayout(
            button_layout
        )  # Add the grid layout to the central layout

        self.load_settings()

    def load_settings(self) -> None:
        """
        Loads settings from the configuration files and initializes the application.
        """
        global formats, path
        recovered_formats, recovered_path = recover_settings()
        if recovered_formats and recovered_path:
            formats, path = recovered_formats, recovered_path
            # Adjust the repo_path_value label's text
            formatted_path = _path_formatted(path)
            self.repo_path_value.setText(formatted_path)
        else:
            formats, path = init_settings()
            # Adjust the repo_path_value label's text
            formatted_path = _path_formatted(path)
            self.repo_path_value.setText(formatted_path)
            if os.path.exists(os.path.join(path, ".gitignore")):
                recover_formats_from_gitignore(path)
            else:
                initialize_git_repo()
            store_settings()

    def check_commits(self) -> None:
        """
        Opens a dialog to check the commits in the repository.
        """
        if path:
            try:
                commit_history = get_commit_history(path)
                dialog = CommitDialog(commit_history)
                dialog.exec_()
            except ValueError:
                QMessageBox.critical(
                    self, "No Commits", "No commits found in the repository."
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"An error occurred: {type(e).__name__} - {str(e)}"
                )
        else:
            QMessageBox.warning(self, "Error", "Repository path is not set.")

    def change_path(self) -> None:
        """
        Changes the repository path.
        """
        global path, formats
        new_path = QFileDialog.getExistingDirectory(
            self, "Select Repository Path", "/.."
        )
        if not new_path or get_absolute_path() == new_path:
            path = os.path.join(get_absolute_path(), "WorkSpace")
            return
        if new_path and not new_path.endswith(("/", "\\")):
            path = new_path
            # Insert newline every 40 chars
            self.repo_path_value.setText(_path_formatted(path))
            if all(os.path.exists(os.path.join(new_path, p)) for p in [".gitignore", ".git"]):
                recover_formats_from_gitignore(new_path)
            else:
                initialize_git_repo()
            # Store the updated settings
            store_settings()
        else:
            return

    def commit_current(self) -> None:
        """
        Commits the current changes in the repository.
        """
        if path:
            now = datetime.datetime.now()
            commit_message = now.strftime("%Y-%m-%d-%H-%M-%S")
            commit_changes(path, commit_message)
            QMessageBox.information(
                self,
                "Commit Successful",
                f"Changes committed with message: {commit_message}",
            )
        else:
            QMessageBox.warning(self, "Error", "Repository path is not set.")

    def change_formats(self) -> None:
        """
        Opens a dialog to change the file formats.
        """
        global formats, path
        if path:
            formats, _ = recover_settings()
            if formats is not None and path is not None:
                # Initialize the dialog window
                dialog = ChangeFormatsDialog(formats)
                if (
                        dialog.exec_() == QDialog.Accepted
                ):  # Check if the dialog was accepted
                    QMessageBox.information(
                        None, "Success", "Formats updated successfully."
                    )
                else:
                    pass
            else:
                QMessageBox.warning(None, "Error", "Unable to recover data.")
        else:
            QMessageBox.warning(self, "Error", "Repository path is not set.")


class ChangeFormatsDialog(QDialog):
    """
    Dialog window for changing file formats.

    """

    def __init__(self, current_formats: List[str], parent: QWidget = None):
        """
        Initialize the dialog window.

        Args:
            current_formats (List[str]): The current list of formats.
            parent (QWidget, optional): The parent widget for the dialog. Defaults to None.
        """
        super().__init__(parent)
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Change File Formats")
        self.setGeometry(200, 200, 400, 300)  # Set a specific size for the dialog
        layout = QVBoxLayout()

        self.setWindowOpacity(0.8125)

        self.text_edit = QPlainTextEdit()
        self.text_edit.setPlainText(
            "\n".join(current_formats)
        )  # Set the current formats
        layout.addWidget(self.text_edit)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(
            self.accept_changes
        )  # Connect the button to the new method
        layout.addWidget(self.ok_button)

        self.setLayout(layout)
        self.ok_button.setStyleSheet(
            "background-color: rgb(20, 32, 48); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, "
            "12); border-radius: 3px; padding: 5px;"
        )
        self.ok_button.setFont(GENERAL_FONT)

        # Set background color to transparent
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(10, 16, 24))
        self.setAutoFillBackground(False)
        self.setPalette(palette)

        # Apply styles and font settings to the dialog
        self.setStyleSheet(
            "background-color: rgb(10, 16, 24); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, 12); padding: "
            "5px;"
        )
        self.text_edit.setFont(GENERAL_FONT)  # Apply bold font to the text edit widget

    def get_new_formats(self) -> List[str]:
        """
        Retrieves the new formats entered by the user.

        Returns:
            List[str]: The list of new formats.
        """
        return [
            line.strip()
            for line in self.text_edit.toPlainText().split("\n")
            if line.strip()
        ]

    def accept_changes(self) -> None:
        """
        Accepts the changes made by the user and updates the formats accordingly.
        """
        new_formats = self.get_new_formats()
        if new_formats:
            store_settings()  # Store the new formats
            update_gitignore()  # Update gitignore
            commit_changes(path, "Updated file formats")  # Commit changes
            QMessageBox.information(self, "Success", "Formats updated successfully.")
        else:
            QMessageBox.warning(self, "Error", "No new formats provided.")


class CommitDialog(QDialog):
    """
    Dialog window for checking commits.
    """

    def __init__(self, commits: List[str]):
        """
        Initialize the dialog window.

        Args:
            commits (List[str]): List of commit history entries.
        """
        super().__init__()
        self.setWindowIcon(get_icon())
        self.setWindowTitle("Check Commits")
        self.setGeometry(200, 200, 400, 300)  # Set a specific size for the dialog
        layout = QVBoxLayout()
        self.commit_list = QListWidget()
        self.hash_list = []  # List to store commit hashes
        self.date_list = []  # List to store formatted dates
        for commit in commits:
            commit_hash, commit_note = commit.split(":")
            self.hash_list.append(commit_hash.strip())
            try:
                commit_date_time = datetime.datetime.strptime(
                    commit_note.strip(), "%Y-%m-%d-%H-%M-%S"
                )
                formatted_date_time = commit_date_time.strftime("%Y/%m/%d, %H:%M")
                self.date_list.append(formatted_date_time + " Version")
            except ValueError:
                self.date_list.append(commit_note.strip() + " Version")
            self.commit_list.addItem(self.date_list[-1])  # Adding to QListWidget
        layout.addWidget(self.commit_list)

        self.setWindowOpacity(0.875)

        # Apply font settings to the QListWidget
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        font.setBold(True)  # Set font to bold
        font.setPointSize(10)  # Set font size to 10
        self.commit_list.setFont(font)  # Apply bold font to the QListWidget

        self.recover_button = QPushButton("Recover", self)
        self.recover_button.clicked.connect(self.recover_commit)
        layout.addWidget(self.recover_button)

        self.recover_button.setFont(GENERAL_FONT)  # Apply font to the "Recover" button

        # Apply styles and font settings to the dialog
        self.setLayout(layout)
        self.setStyleSheet(
            "background-color: rgb(10, 16, 24); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, 12); padding: "
            "5px;"
        )
        self.recover_button.setStyleSheet(
            "background-color: rgb(48, 60, 78); color: rgb(227, 239, 255); border: 2px solid rgb(5, 8, "
            "12); border-radius: 3px; padding: 5px;"
        )

    def recover_commit(self) -> None:
        """
        Attempts to recover the selected commit from the repository.
        """
        current_index = self.commit_list.currentRow()
        if current_index >= 0:
            selected_commit_hash = self.hash_list[current_index]
            try:
                recover_commit_local(selected_commit_hash)
                QMessageBox.information(
                    self,
                    "Recovery Successful",
                    "Selected commit has been recovered successfully.",
                )
            except RuntimeError as error:
                QMessageBox.warning(self, "Error", str(error))


def recover_commit_local(commit_hash: str) -> None:
    """
    Attempts to recover the repository to the state of the specified commit.

    Args:
        commit_hash (str): The hash of the commit to recover to.

    Raises:
        RuntimeError: If an error occurs while recovering the commit.
    """
    repo_path = (
        path  # Assuming path is a global variable accessible within CommitDialog
    )
    repo = Repo(repo_path)
    try:
        repo.git.reset("--hard", commit_hash)
    except Exception as e:
        raise RuntimeError(f"Error recovering commit: {e}")


def get_commit_history(repo_path: str) -> List[str]:
    """
    Retrieves the commit history of the repository.

    Args:
        repo_path (str): The path to the repository.

    Returns:
        List[str]: A list of commit history entries.
    """
    repo = Repo(repo_path)
    commits = repo.iter_commits()
    commit_list = []
    for commit in commits:
        commit_list.append(f"{commit.hexsha}: {commit.message.strip()}")
    return commit_list


def make_hash_settings(_formats: List[str], _path: str) -> str:
    """
    Generates a SHA-256 hash value based on the formats and path.

    Args:
        _formats (List[str]): List of file formats.
        _path (str): The repository path.

    Returns:
        str: The SHA-256 hash value.
    """
    formats_str = "\n".join(_formats)
    data = formats_str + _path
    hash_object = hashlib.sha256(data.encode())
    hash_str = hash_object.hexdigest()
    return hash_str


def store_settings() -> None:
    """
    Stores the current settings to a .dat file.
    """
    global formats, path
    hash_str = make_hash_settings(formats, path)
    data = {"formats": formats, "path": path, "hash_str": hash_str}
    with open(os.path.join(get_absolute_path(), "data.dat"), "wb") as f:
        pickle.dump(data, f)


def recover_settings() -> Tuple[Optional[List[str]], Optional[str]]:
    """
    Attempts to recover settings from the .dat file.

    Returns:
        Tuple[Optional[List[str]], Optional[str]]: A tuple containing recovered formats and path.
    """
    try:
        with open(os.path.join(get_absolute_path(), "data.dat"), "rb") as f:
            recovered_data = pickle.load(f)
            recovered_formats = recovered_data["formats"]
            recovered_path = recovered_data["path"]
            recovered_hash_str = recovered_data["hash_str"]
        if make_hash_settings(recovered_formats, recovered_path) == recovered_hash_str:
            return recovered_formats, recovered_path
        else:
            return None, None
    except FileNotFoundError:
        return None, None


def get_initial_directory() -> str:
    """
    Retrieves the initial directory for the file dialog.

    Returns:
        str: The initial directory path.
    """
    return QFileDialog.getExistingDirectory(None, "Select Folder", path)


def init_settings() -> Tuple[List[str], str]:
    """
    Initializes default settings.

    Returns:
        Tuple[List[str], str]: A tuple containing default formats and path.
    """
    global formats, path
    formats = [".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".txt"]
    path = get_initial_directory()
    return formats, path


def initialize_git_repo() -> None:
    """
    Initializes a Git repository.
    """
    global formats, path
    repo = Repo.init(path)
    git = repo.git
    git.checkout(b="master")
    update_gitignore()
    commit_changes(path, "initial commit")


def update_gitignore() -> None:
    """
    Updates the .gitignore file with the current formats.
    """
    global formats, path
    gitignore_path = os.path.join(path, ".gitignore")
    with open(gitignore_path, "w") as f:
        for file_format in formats:
            f.write("!" + file_format + "\n")
        f.write("*\n")


def commit_changes(_path: str, message: str) -> None:
    """
    Commits changes to the repository.

    Args:
        _path (str): The path to the repository.
        message (str): The commit message.
    """
    try:
        repo = Repo(_path)
        repo.git.add("--all")
        repo.index.commit(message)
    except Exception as e:
        raise ("Error committing changes:", e)


def main() -> None:
    """
    Main function to launch the application.
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    try:
        app.exec_()
    finally:
        # Cleanup subprocesses
        QCoreApplication.processEvents()
        QCoreApplication.quit()
        sys.exit()


if __name__ == "__main__":
    main()
