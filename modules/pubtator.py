import requests
import xml.etree.ElementTree as ET


# check candidate species from the specific section
def get_annotation_from_section(element, section:str):
    """
    Parameters:
    -------------
    element:XML
    section:str

    Returns:
    ----------------
    elements:list
        A list of elements of annotations in the specific section
    
    """
    passages = element.findall("passage")
    for passage in passages:
        if passage.find("infon[@key='type']").text == section:
            annotations = passage.findall("annotation")
        else:
            continue
    return annotations


# check candidate genes and diseases from title and abstract sections
def get_annotation_ptc(element):
    """
    Parameters:
    -------------
    element:XML

    Returns:
    ----------------
    species:list
        a list of annotation genes and diseases in title and abstract sections
    """
    genes = []
    disease = []
    cellline = []
    for passage in element:
        ans = passage.findall("annotation")

        for a in ans:
            if a.find("infon[@key='type']").text == "Gene":
                try:
                    genes.append(a.find("infon[@key='identifier']").text)
                except:
                    continue

            if a.find("infon[@key='type']").text == "Disease":
                try:
                    disease.append(a.find("text").text)
                except:
                    continue
            
            if a.find("infon[@key='type']").text == "Cellline":
                try:
                    cellline.append(a.find("text").text)
                except:
                    continue

    return genes, disease, cellline


