##!/usr/bin/env python3
import requests
import unittest

class TestRedirects(unittest.TestCase):
    def test_index_request(self):
        url = "https://w3id.org/CEON"
        expected = "https://liusemweb.github.io/CEON/"
        r = requests.head(url, allow_redirects=True)
        self.assertEqual(r.url, expected)
    
    def test_catalogue_request(self):
        url = "https://w3id.org/CEON/catalogue"
        expected = "https://liusemweb.github.io/CEON/catalogue"
        r = requests.head(url, allow_redirects=True)
        self.assertEqual(r.url, expected)
    
    def test_catalogue_item_request(self):
        url = "https://w3id.org/CEON/catalogue/example"
        expected = "https://liusemweb.github.io/CEON/catalogue/example"
        r = requests.head(url, allow_redirects=True)
        self.assertEqual(r.url, expected)
    
    def test_ontology_request(self):
        url = "https://w3id.org/CEON/ontology/example/"
        accept = "text/turtle"
        expected = "https://liusemweb.github.io/CEON/ontology/example/latest/example.ttl"
        r = requests.head(url, allow_redirects=True, headers={"Accept": accept})
        self.assertEqual(r.url, expected)
    
    def test_versioned_ontology_request(self):
        url = "https://w3id.org/CEON/ontology/example/1.0/"
        accept = "text/turtle"
        expected = "https://liusemweb.github.io/CEON/ontology/example/1.0/example.ttl"
        r = requests.head(url, allow_redirects=True, headers={"Accept": accept})
        self.assertEqual(r.url, expected)
    
    def test_docs_request(self):
        url = "https://w3id.org/CEON/ontology/example/"
        expected = "https://liusemweb.github.io/CEON/ontology/example/latest/index.html"
        r = requests.head(url, allow_redirects=True)
        self.assertEqual(r.url, expected)
    
    def test_versioned_docs_request(self):
        url = "https://w3id.org/CEON/ontology/example/1.0/"
        expected = "https://liusemweb.github.io/CEON/ontology/example/1.0/index.html"
        r = requests.head(url, allow_redirects=True)
        self.assertEqual(r.url, expected)


if __name__ == '__main__':
    unittest.main()