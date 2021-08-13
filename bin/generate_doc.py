from tomark import Tomark

from symbench_athens_client.models.designs import (HCopter, HPlane, QuadCopter,
                                                   QuadSpiderCopter)


class DocsGenerator:
    @staticmethod
    def generate_for_design(seed_design_classes):
        md = ["# Seed designs"]
        for cls in seed_design_classes:
            md.append(f"\n## {cls.__name__}")
            md.append(f"\n{cls.__doc__}\n")
            md.append(f"\n Parameters are listed below:\n")
            fields = []
            for field, field_info in cls.__fields__.items():
                if field != "name" and field != "swap_list":
                    fields.append(
                        {
                            "name": field,
                            "Name in Graph": field_info.alias,
                            "default": field_info.default
                            if field in cls.__design_vars__
                            else field_info.default.name,
                        }
                    )

            md.append(Tomark.table(fields))
            md.append("\n\n### Jenkins Design Variables and Defaults:")
            md.append(Tomark.table([cls().to_jenkins_parameters()]))
            md.append("\n\n")
        return "\n".join(md)


if __name__ == "__main__":
    from pathlib import Path

    DOCS_BASE = Path(__file__).parent.resolve() / ".." / "docs"
    designs_md = DocsGenerator.generate_for_design(
        [QuadCopter, QuadSpiderCopter, HCopter, HPlane]
    )
    with open(DOCS_BASE / "seed_designs.md", "w") as d_file:
        d_file.write(designs_md)
