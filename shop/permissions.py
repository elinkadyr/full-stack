from rest_framework.permissions import BasePermission

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
    

"""
Класс IsAuthor наследуется от базового класса BasePermission.

Метод has_object_permission в классе IsAuthor 
        определяет логику проверки доступа к объекту. 
Он принимает три параметра: 
        request (объект запроса), 
        view (объект представления),
        obj (объект модели, к которому осуществляется доступ).

Внутри метода has_object_permission выполняется сравнение между пользователем, 
            указанным в запросе (request.user), 
            и пользователем, связанным с объектом (obj.user). 
    
    Если они совпадают, то метод возвращает True, доступ разрешен. 
    Если пользователи различаются - False, доступ запрещен.

"""