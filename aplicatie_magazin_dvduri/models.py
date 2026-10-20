from datetime import date

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class Gen(models.Model):
    """Categoria filmelor (entitatea 'Gen' din diagrama)."""

    VARSTE = [
        (0, "Toate varstele"),
        (12, "12+"),
        (15, "15+"),
        (18, "18+"),
    ]

    nume = models.CharField(
        max_length=50,
        unique=True,
        help_text="Numele genului, unic (ex: Comedie, Actiune).",
        error_messages={
            "unique": "Exista deja un gen cu acest nume.",
            "max_length": "Numele genului poate avea cel mult 50 de caractere.",
        },
    )
    descriere = models.TextField(blank=True)
    culoare = models.CharField(
        max_length=7,
        default="#8b5a3c",
        validators=[RegexValidator(r"^#[0-9a-fA-F]{6}$", "Culoarea trebuie sa fie de forma #rrggbb.")],
        help_text="Cod hex al culorii reprezentative, folosita la stilizare (ex: #ff0000).",
    )
    sigla = models.CharField(
        max_length=50,
        default="fa-film",
        help_text="Numele unui icon din FontAwesome (ex: fa-film, fa-ghost).",
    )
    varsta_minima = models.PositiveSmallIntegerField(
        choices=VARSTE,
        default=0,
        help_text="Varsta minima recomandata pentru filmele din acest gen.",
    )

    class Meta:
        ordering = ["nume"]
        verbose_name_plural = "Genuri"
        constraints = [
            models.CheckConstraint(
                condition=Q(varsta_minima__gte=0) & Q(varsta_minima__lte=18),
                name="gen_varsta_minima_0_18",
                violation_error_message="Varsta minima trebuie sa fie intre 0 si 18.",
            ),
        ]

    def __str__(self):
        return self.nume


class Studio(models.Model):
    """Producatorul filmului."""

    nume = models.CharField(
        max_length=100,
        unique=True,
        error_messages={"unique": "Acest studio exista deja in baza de date."},
    )
    tara = models.CharField(max_length=60)
    an_infiintare = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Lasati liber daca anul infiintarii nu se cunoaste.",
    )
    website = models.URLField(
        null=True,
        blank=True,
        error_messages={"invalid": "Introduceti o adresa web valida (ex: https://studio.com)."},
    )

    class Meta:
        ordering = ["nume"]
        verbose_name_plural = "Studiouri"
        indexes = [models.Index(fields=["tara"])]
        constraints = [
            models.CheckConstraint(
                condition=Q(an_infiintare__isnull=True)
                | (Q(an_infiintare__gte=1850) & Q(an_infiintare__lte=2100)),
                name="studio_an_infiintare_valid",
                violation_error_message="Anul infiintarii trebuie sa fie intre 1850 si 2100.",
            ),
        ]

    def __str__(self):
        return self.nume


class Distribuitor(models.Model):
    """Companie partenera care distribuie o parte din filme."""

    nume = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "Exista deja un distribuitor cu acest email.",
            "invalid": "Introduceti o adresa de email valida.",
        },
    )
    telefon = models.CharField(max_length=20, null=True, blank=True)
    data_parteneriat = models.DateField(
        default=date.today,
        help_text="Data de la care colaboram cu distribuitorul (implicit, azi).",
    )

    class Meta:
        verbose_name_plural = "Distribuitori"

    def __str__(self):
        return self.nume


class Magazin(models.Model):
    """Sediile companiei."""

    nume = models.CharField(max_length=100)
    adresa = models.CharField(max_length=200)
    oras = models.CharField(max_length=60)
    telefon = models.CharField(max_length=20, null=True, blank=True)
    program = models.CharField(
        max_length=100,
        default="L-V 10:00-20:00",
        blank=True,
        help_text="Programul de lucru. Poate fi lasat liber daca nu este stabilit.",
    )

    class Meta:
        ordering = ["oras", "nume"]
        verbose_name_plural = "Magazine"
        indexes = [models.Index(fields=["oras"])]

    def __str__(self):
        return f"{self.nume} ({self.oras})"


class Raion(models.Model):
    """Entitate slaba: se identifica prin (magazin, nume)."""

    magazin = models.ForeignKey(Magazin, on_delete=models.CASCADE, related_name="raioane")
    nume = models.CharField(max_length=60)
    etaj = models.PositiveSmallIntegerField(default=0, help_text="0 = parter.")
    capacitate_rafturi = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Numarul maxim de rafturi; lasati liber daca nu e stabilit.",
    )
    gen = models.ForeignKey(
        Gen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="raioane",
        help_text="Genul de filme caruia ii este dedicat raionul.",
    )

    class Meta:
        verbose_name_plural = "Raioane"
        constraints = [
            models.UniqueConstraint(
                fields=["magazin", "nume"],
                name="raion_nume_unic_in_magazin",
                violation_error_message="Magazinul are deja un raion cu acest nume.",
            ),
            models.CheckConstraint(
                condition=Q(capacitate_rafturi__isnull=True) | Q(capacitate_rafturi__gt=0),
                name="raion_capacitate_pozitiva",
                violation_error_message="Capacitatea trebuie sa fie mai mare ca 0.",
            ),
        ]

    def __str__(self):
        return f"{self.nume} - {self.magazin.nume}"


class Eveniment(models.Model):
    """Eveniment organizat intr-un magazin, care promoveaza produsele."""

    magazin = models.ForeignKey(Magazin, on_delete=models.CASCADE, related_name="evenimente")
    titlu = models.CharField(max_length=120)
    descriere = models.TextField(blank=True)
    data_inceput = models.DateTimeField(default=timezone.now)
    data_sfarsit = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Lasati liber pentru un eveniment fara data de sfarsit stabilita.",
    )

    class Meta:
        verbose_name_plural = "Evenimente"
        indexes = [models.Index(fields=["data_inceput"])]
        constraints = [
            models.CheckConstraint(
                condition=Q(data_sfarsit__isnull=True) | Q(data_sfarsit__gte=F("data_inceput")),
                name="eveniment_sfarsit_dupa_inceput",
                violation_error_message="Data de sfarsit nu poate fi inainte de data de inceput.",
            ),
        ]

    def __str__(self):
        return self.titlu


class Film(models.Model):
    """Produsul vandut."""

    FORMATE = [
        ("DVD", "DVD"),
        ("BLURAY", "Blu-ray"),
        ("4K", "4K UHD"),
    ]

    titlu = models.CharField(
        max_length=200,
        error_messages={
            "blank": "Filmul trebuie sa aiba un titlu.",
            "max_length": "Titlul poate avea cel mult 200 de caractere.",
        },
    )
    descriere = models.TextField(blank=True)
    an_aparitie = models.PositiveSmallIntegerField(
        error_messages={"invalid": "Anul aparitiei trebuie sa fie un numar intreg."},
    )
    durata_minute = models.PositiveSmallIntegerField(
        help_text="Durata filmului, in minute.",
    )
    pret = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Pretul in lei, cu cel mult 2 zecimale.",
        error_messages={"invalid": "Pretul trebuie sa fie un numar (ex: 49.99)."},
    )
    format = models.CharField(max_length=6, choices=FORMATE, default="DVD")
    data_adaugare = models.DateTimeField(default=timezone.now)
    in_stoc = models.BooleanField(default=True)
    actori = models.JSONField(
        default=list,
        blank=True,
        help_text='Lista actorilor, ca lista JSON (ex: ["Actor 1", "Actor 2"]).',
    )
    coperta = models.ImageField(upload_to="coperte/", null=True, blank=True)

    gen = models.ForeignKey(Gen, on_delete=models.PROTECT, related_name="filme")
    studio = models.ForeignKey(
        Studio, on_delete=models.SET_NULL, null=True, blank=True, related_name="filme"
    )
    distribuitori = models.ManyToManyField(Distribuitor, blank=True, related_name="filme")

    class Meta:
        ordering = ["titlu"]
        verbose_name_plural = "Filme"
        indexes = [
            models.Index(fields=["titlu"]),
            models.Index(fields=["an_aparitie"]),
            models.Index(fields=["pret"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(pret__gt=0),
                name="film_pret_pozitiv",
                violation_error_message="Pretul trebuie sa fie mai mare ca 0.",
            ),
            models.CheckConstraint(
                condition=Q(durata_minute__gte=1) & Q(durata_minute__lte=600),
                name="film_durata_1_600",
                violation_error_message="Durata trebuie sa fie intre 1 si 600 de minute.",
            ),
            models.CheckConstraint(
                condition=Q(an_aparitie__gte=1888) & Q(an_aparitie__lte=2100),
                name="film_an_aparitie_valid",
                violation_error_message="Anul aparitiei trebuie sa fie intre 1888 si 2100.",
            ),
        ]

    def __str__(self):
        return f"{self.titlu} ({self.an_aparitie})"