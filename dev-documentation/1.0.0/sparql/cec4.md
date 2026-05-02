# Circular Enabler Category 4 – SPARQL Queries

All queries assume the [common prefixes](index.md#prefixes) are declared.

---

## CQ-CE-10-1

**What capacity (e.g. competence) is needed from actors in order to collaborate?**

```sparql
SELECT ?capability ?actor
WHERE{
    ?capability actorODP:capabilityOf ?actor .
}
```

---

## CQ-CE-10-2

**What information is needed to collaborate and align processes?**

---

## CQ-CE-10-3

**What material or energy flow uses a certain (type of) infrastructure?**

---

## CQ-CE-10-4

**What is the infrastructure available to, or held by, a certain actor?**

```sparql
SELECT ?actor ?infra
WHERE{
    ?participation actorODP:participatingInfrastructure ?infra .
    ?participation actorODP:participatingActor ?actor .
}
```

---

## CQ-CE-10-5

**What capacity of infrastructure is unused and can be shared with others?**

---

## CQ-CE-10-6

**What are the alignments between processes across actors, e.g. matching inputs and outputs, time etc?**

```sparql
SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10
```

---

## CQ-CE-10-7

**What are the energy outputs of an actor/process?**

```sparql
SELECT ?process ?energy
WHERE {
    ?energy rdf:type process:Energy .
    ?process processODP:hasOutput ?energy .
}
```

---

## CQ-CE-10-8

**What is the potential for energy recovery?**

---

## CQ-CE-10-9

**What energy surplus/demand does an actor have?**

---

## CQ-CE-10-10

**What value can be (co)created/transferred/captured by and actor or a collaboration?**

- **Same as:** [CQ-CE-5-17.sparql](../sparql/cec2.md#cq-ce-5-17)

---

## CQ-CE-11-1

**What capacity (e.g. competence) is needed to ingrate an acor in the network?**

---

## CQ-CE-11-2

**What is the value created (incentive) for a certain actor in a certain collaboration/process?**

- **Same as:** [CQ-CE-5-17.sparql](../sparql/cec2.md#cq-ce-5-17)

---

## CQ-CE-11-3

**What information does a certain actor hold, or have access to?**

```sparql
SELECT ?resource
WHERE{
    ?resourceRelation actorODP:participatingResource ?resource .
    ?resourceRelation actorODP:participatingActor ?actor .
}
```

---

## CQ-CE-11-4

**What is the access control information for this piece of information/who do I share the information with?**

---

## CQ-CE-11-5

**For what is this information needed/used?**

```sparql
SELECT ?process ?information
WHERE{
    ?process processODP:hasInput ?information .
}
```

---

## CQ-CE-11-6

**Who and hos is energy contributed to this process?**

---

## CQ-CE-11-7

**Who is consuming/using this product?**

```sparql
SELECT ?process ?actor ?product
WHERE{
    ?process processODP:hasInput ?product.
    ?collaboration actorODP:participationIn ?process.
    ?collaboration actorODP:participatingActor ?actor.
}
```

---

## CQ-CE-11-8

**How is the product used?**

---

## CQ-CE-11-9

**How was usage data collected?**

---

## CQ-CE-11-10

**What is the potential/observed/confimed value of this material/component/product or process/action/collaboration to a certain actor?**

- **Same as:** [CQ-CE-5-17.sparql](../sparql/cec2.md#cq-ce-5-17)

---

## CQ-CE-11-11

**Who evaluated the value and by what method?**

---