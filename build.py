from builder.builder import Builder

SITE_NAME = "Sigrid Joubert"

if __name__ == "__main__":
    builder = Builder(SITE_NAME)
    builder.build_site()
