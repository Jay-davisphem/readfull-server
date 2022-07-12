# Database Models

- User #

- Profile:
  - user # OneToOneField
  - profile pics # ImageField
  - followers #
  - following
  - read_count

- Novel
  - title # CharField
  - image # ImageField
  - description # CharField
  - chapters # ForeignKey
  - status # Enum Choices
  - rating # DecimalField
  - view_count #BigIntegerField
  - genre # Enum Choice
  - author # ManyToMany
  - alt_names # CharField
  - source # CharField

- Chapter
  - title # CharField
  - chapter_number # IntegerField
  - content # CharField
  - likes # Enum Choices (Interesting, Somewhat Interesting, Biased, Normal, Boring)

- Comment
  - chapter # ForeignKey
  - commentor # OneToOneField
  - message
  - reponse # proly

- CommenResponse
  - responder
  - comment
  - message
  - created
  - updated
