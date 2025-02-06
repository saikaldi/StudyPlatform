from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TestCategoryViewSet,
    TestViewSet,
    TestContentViewSet,
    TestFullDescriptionViewSet,
    UserAnswerViewSet,
    UserStatisticViewSet,
    SubjectCategoryViewSet,
    OkupTushunuuViewSet,
    OkupTushunuuQuestionViewSet,
    OkupTushunuuTextViewSet,
    TestInstructionViewSet
)


router = DefaultRouter()
router.register(r"testcategories", TestCategoryViewSet, basename="testcategory")
router.register(r"subjectcategories", SubjectCategoryViewSet, basename="subjectcategory")
router.register(r"tests", TestViewSet, basename="test")
router.register(r"TestContent", TestContentViewSet, basename="TestContent")
router.register(r"test-instruction", TestInstructionViewSet, basename="testinstruction")
router.register(r"testfulldescriptions", TestFullDescriptionViewSet, basename="testfulldescription")
router.register(r"useranswers", UserAnswerViewSet, basename="useranswer")
router.register(r"userstatistics", UserStatisticViewSet, basename="userstatistics")
router.register(r"okup-tushunuu-text", OkupTushunuuTextViewSet, basename="OkupTushunuuText")
router.register(r"okup-tushunuu", OkupTushunuuViewSet, basename="okup-tushunuu")
router.register(r"okup-tushunuu-questions", OkupTushunuuQuestionViewSet, basename="okup-tushunuu-question")

urlpatterns = [
    path("", include(router.urls)),
]
