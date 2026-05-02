# Circular Enabler Category 3 – SPARQL Queries

All queries assume the [common prefixes](index.md#prefixes) are declared.

---

## CQ-CE-8-1

**What are the actions/decisions made by a certain actor at a certain point in time, in relation to a certain collaboration/process/material etc.?**

```sparql
SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10
```

---

## CQ-CE-8-2

**What is the energy input/usage/surplus during a certain life cycle phase of a material/component/product?**

```sparql
SELECT ?process ?energy
WHERE {
    ?energy rdf:type process:Energy .
    ?process process:needsEnergy ?energy .
}
```

---

## CQ-CE-8-3

**Why should an actor share certain data?**

```sparql
SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10
```

---

## CQ-CE-9-1

**What are the characteristics, including quality, of this material?**

```sparql
SELECT ?resource ?quality
WHERE {
    ?resource rdf:type resourceODP:Resource .
    ?resource resourceODP:hasResourceQuality ?quality .
}
```

---

## CQ-CE-9-2

**What is the data of this energy flow at this point in time?**

```sparql
SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10
```

---

## CQ-CE-9-3

**How efficient is this process?**

---

## CQ-CE-9-4

**What kinds of value are involved in this collaboration/process?**

- **Same as:** [CQ-CE-5-16.sparql](../sparql/cec2.md#cq-ce-5-16)

---

## CQ-CE-9-5

**What are the needs underlying this value/collaboration/process?**

```sparql
SELECT ?resource
WHERE{
    ?process processODP:hasInput ?resource .
}
```

---