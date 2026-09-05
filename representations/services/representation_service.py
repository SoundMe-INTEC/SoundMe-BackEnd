from dictionary.models.sign import Sign
from representations.repositories.representations_repository import RepresentationRepository
from representations.models.representation import Representation


class RepresentationService:

    def __init__(self):
        self._repre_repo = RepresentationRepository()

    def find_all(self):
        return self._repre_repo.get_all()

    def find_all_active(self):
        return self._repre_repo.get_all_active()

    def find_by_id(self, sign_id):
        repre = self._repre_repo.get_by_id(sign_id)

        if repre is None:
            raise ValueError("Representation doesn't exist")

        return repre

    def find_by_pk(self, representation_id):
        repre = self._repre_repo.get_by_pk(representation_id)

        if repre is None:
            raise ValueError("Representation doesn't exist")

        return repre

    def create(self, data, user, sign):
        if not sign:
            raise ValueError("sign_id is required")

        sign_obj = sign if isinstance(sign, Sign) else Sign.objects.filter(id=sign).first()

        if sign_obj is None:
            raise ValueError("Sign doesn't exist")

        repre = Representation(
            sign_id=sign_obj,
            create_by=user,
            extension=data["extension"],
            url=data["url"]
        )

        return self._repre_repo.create(repre)

    def update(self, sign_id, data):
        repre = self._repre_repo.get_by_id(sign_id)

        if repre is None:
            raise ValueError("Representation doesn't exist")

        new_url = data.get("url")

        if new_url and new_url != repre.url:
            repre.url = new_url

        new_extension = data.get("extension")

        if new_extension and new_extension != repre.extension:
            repre.extension = new_extension

        allowed_to_change = ("url", "extension")

        for field in allowed_to_change:
            if field in data:
                setattr(repre, field, data[field])

        return self._repre_repo.update(repre)

    def update_by_pk(self, representation_id, data):
        repre = self.find_by_pk(representation_id)

        allowed_to_change = ("url", "extension", "is_primary", "order")

        for field in allowed_to_change:
            if field in data:
                setattr(repre, field, data[field])

        return self._repre_repo.update(repre)

    def deactivate(self, representation_id):
        repre = self.find_by_pk(representation_id)
        repre.is_active = False
        return self._repre_repo.update(repre)

    def activate(self, representation_id):
        repre = self.find_by_pk(representation_id)
        repre.is_active = True
        return self._repre_repo.update(repre)

    def soft_delete(self, sign_id):
        is_delete = self._repre_repo.soft_delete(sign_id)

        return (
            f"repre: {sign_id} has been deleted"
            if is_delete
            else "Representation could not be found"
        )

    def soft_delte(self, sign_id):
        return self.soft_delete(sign_id)
        