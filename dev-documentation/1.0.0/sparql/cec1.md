# Circular Enabler Category 1 – SPARQL Queries

All queries assume the [common prefixes](index.md#prefixes) are declared.

---



## CQ-CE-1-1

**What are the connections and dependencies between actors and processes in a certain value network?**

```sparql
SELECT ?actor ?role
WHERE{
    ?actor rdf:type actorODP:Actor .
    ?participation rdf:type actorODP:Participation .
    ?participation actorODP:participatingActor ?actor .
    ?participation actorODP:participantRole ?role .
    ?role rdf:type actorODP:Role .
    ?participation actorODP:participationIn cvn:Colloboration .
}
```

---

## CQ-CE-1-2

**What is the energy components in this system, e.g. exergy and anergy?**

```sparql
SELECT ?component ?exergy ?anergy
WHERE{
    ?component energy:hasExergy ?exergy .
    ?component energy:hasAnergy ?anergy .
}
```

---

## CQ-CE-1-3

**What are the involved value forms, e.g. economic, social, environmental?**

```sparql
SELECT ?value
WHERE{
    ?cvn rdf:type cvn:CVN .
    ?cvn cvn:createsValue ?value .
    ?value rdf:type value:Value .
}
```

---

## CQ-CE-2-1

**What are the actors (and their roles) in the value network?**

- **Same as:** [CQ-CE-1-1.sparql](../sparql/cec1.md#cq-ce-1-1)

---

## CQ-CE-2-2

**What are the connections and dependencies between actors and materials/components/products in a certain value network?**

- **Same as:** [CQ-CE-1-1.sparql](../sparql/cec1.md#cq-ce-1-1)

---

## CQ-CE-3-1

**What is the value network implementing in terms of circular strategies?**

```sparql
SELECT ?strategy
WHERE{
    ?cvn rdf:type cvn:CVN .
    ?cvn cvn:implementsStrategy ?strategy .
    ?strategy rdf:type cvn:CircularStrategy .
}
```

---

## CQ-CE-3-2

**What is the process breakdown of this life cycle (what processes are involved and in what order), across actors?**

```sparql
SELECT ?process ?prevproc ?nextproc
WHERE {
    ?process rdf:type process:TransformationProcess .
    OPTIONAL {
        ?nextproc rdf:type process:TransformationProcess .
        ?prevproc processODP:nextProcess ?nextproc . 
    }
    OPTIONAL {
        ?prevproc rdf:type processODP:Transformation .
        ?prevproc processODP:nextProcess ?process .
    }
    ?participation actorODP:participationIn ?process .
    ?participation actorODP:participatingActor ?actor.
}
```

---

## CQ-CE-3-3

**What is the status and location of this material at this point in time?**

```sparql
SELECT ?resource ?location
WHERE {
    ?resource rdf:type resourceODP:Resource .
    ?resource location:hasLocation ?Location . 
}
```

---

## CQ-CE-3-4

**What are the elements (e.g. steps/work and actors) involved in this process?**

```sparql
SELECT ?participation ?component 
WHERE{
    ?process rdf:type processODP:Process .
    ?participation actorODP:participationIn ?process .
    { ?participation actorODP:participatingActor ?component }
    UNION
    { ?participation actorODP:participatingResource ?component }
}
```

---

## CQ-CE-3-5

**What is the status and location of this material at this point in time?**

```sparql
SELECT ?process ?input ?output 
WHERE{
    ?process rdf:type processODP:Process .
    { ?process processODP:hasInput ?input }
    UNION
    { ?process processODP:hasOutput ?output }
}
```

---

## CQ-CE-4-1

**What are the related circular strategies of this and other related value networks?**

```sparql
SELECT ?cvn ?strategy
WHERE{
    ?cvn rdf:type cvn:CVN .
    ?cvn cvn:composedOf ?cvn .
    ?strategy rdf:type cvn:CircularStrategy .
    ?cvn cvn:implementsStrategy ?strategy .
}
```

---

## CQ-CE-4-2

**What are the connections and dependencies between actors and materials/components/products in a certain value network?**

- **Same as:** [CQ-CE-1-1.sparql](../sparql/cec1.md#cq-ce-1-1)

---

## CQ-CE-4-3

**What is the carbon intensity and other sustainability factors of this energy source?**

```sparql
SELECT ?source ?carbonIntensity ?sustainability
WHERE {
  ?energy rdf:type energy:Energy .
  ?energy energy:hasEnergySource ?source .
  { ?source energy:hashasCarbonIntensity ?carbonIntensity }
  UNION
  { ?source energy:Sustainability ?sustainability }
}
```

---

## CQ-CE-4-4

**What are the elements (e.g. steps/work and actors) involved in this process?**

- **Same as:** [CQ-CE-3-4.sparql](../sparql/cec1.md#cq-ce-3-4)



