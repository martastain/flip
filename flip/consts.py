import enum


class FlipperCommands(enum.Enum):
    led = "led"
    loader = "loader"
    bt = "bt"
    log = "log"
    crypto = "crypto"
    nfc = "nfc"
    date = "date"
    onewire = "onewire"
    device_info = "device_info"
    power = "power"
    factory_reset = "factory_reset"
    ps = "ps"
    free = "free"
    rfid = "rfid"
    free_blocks = "free_blocks"
    source = "source"
    gpio = "gpio"
    start_rpc_session = "start_rpc_session"
    help = "help"
    storage = "storage"
    i2c = "i2c"
    subghz = "subghz"
    ikey = "ikey"
    sysctl = "sysctl"
    info = "info"
    update = "update"
    input = "input"
    uptime = "uptime"
    ir = "ir"
    vibro = "vibro"
