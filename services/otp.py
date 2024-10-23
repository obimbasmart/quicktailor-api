from services.cache import cache
from random import randint


class OTPService:
    __expires_in = 180

    def generate_and_store_otp(self, email: str) -> str:
        otp = self.__generate_otp()
        cache.store(f"otp:{email}", otp, expires=self.__expires_in)
        return otp

    def verify_otp(self, email: str, otp: str) -> bool:
        redis_otp = cache.get(f"otp:{email}", cache.get_str)
        return redis_otp == otp

    def __generate_otp(self):
        return randint(100000, 999999)
    

otp_service = OTPService()
