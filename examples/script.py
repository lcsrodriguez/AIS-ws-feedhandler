from AIS import *


if __name__ == "__main__":
    try:
        asyncio.run(connect_ais_stream())
    except KeyboardInterrupt:
        print("KBI")
    finally:
        #u = Usage().getUsage()
        pass
