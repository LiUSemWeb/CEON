# Methodology

CEON is developed using a combination of two agile ontology engineering methodologies: **eXtreme Design (XD)** and **Modular Ontology Modeling (MOMo)**. This combination was chosen based on an analysis of the Onto-DESIDE project requirements and structure.

The combination includes:

- Adopting **rapid prototyping** and a **requirements-driven approach** from XD
- Following the overall outline from **MOMo**, including identifying existing Ontology Design Patterns (ODPs) and creating module diagrams

## Why This Combination?

The Onto-DESIDE project had three evaluation iterations, making an agile methodology a natural fit — one that prioritizes flexibility, domain expert requirements, and rapid iterative delivery. Furthermore, the project requirements highlighted the need for **cross-domain modeling** spanning topics such as resources, processes, circular value networks, and dedicated industry use cases (construction, electronics, and textile). An ontology network with general ODPs addresses cross-domain interoperability while maintaining suitable modeling granularity.

Other methodologies such as **LOT** (Linked Open Terms) and **SAMOD** were considered. XD was selected as the most suitable since it combines agile development principles with the use of ODPs. Although LOT was not explicitly followed, an ontology development and publishing pipeline was set up to satisfy the **FAIR principles** (Findable, Accessible, Interoperable, and Reusable), making the work generally aligned with LOT as well.

## Requirements Analysis

The Onto-DESIDE project requirements span multiple perspectives:

=== "Top-down (CE Requirements)"
    13 **CE requirements** (circular enablers) were developed based on general CE terminology and concepts used in standards and value flow analysis methodologies such as Circularity Thinking. These represent cross-domain challenges and circularity concepts.

=== "Bottom-up (Use Case Requirements)"
    44 **use-case requirements** were developed across the three industry domains:

    | Domain | Requirements |
    |---|---|
    | Construction | 13 |
    | Electronics | 6 |
    | Textile | 23 |

The requirements were then mapped to **9 topics**:

- Circular value network
- Value
- Actor
- Process
- Material
- Product
- Location
- Quantities and units
- Provenance

Based on these topics, relevant **Competency Questions (CQs)**, contextual statements, and reasoning statements were proposed. The latest set of ontological requirements includes **90 CQs** across 13 CE requirements. Use-case related CQs were also proposed for developing the use-case ontologies.

### Example CE Requirements and CQs

| CE Requirement | Competency Questions |
|---|---|
| The capacity to understand interrelations between processes and actors in the system | What are the connections and dependencies between actors and processes in a certain value network? What are the energy components in this system, e.g., exergy and anergy? |
| The capacity to identify and consider all (relevant) system actors | What are the actors (and their roles) in the value network? What are the connections and dependencies between actors and materials/components/products in a certain value network? |
| The capacity to consider processes throughout entire life cycle | What is the value network implementing in terms of circular strategies? What is the process breakdown of this life cycle? |
| The capacity to develop new configurations | What are the characteristics, including quality, of this material? What kinds of value are involved in this collaboration/process? |

