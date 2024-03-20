Basic Usage
===========

Command Line
------------

The easiest way to use Dpai is through command line. It involves two steps for automatic api generation:

#. Step 1. Register your model details. You can register multiple models.

.. code-block::
    
    dpai register -n your_model_name -m your_model_path -i your_inference_path

#. Step 2. Setup API endpoints and spin up a server, each model corresponds to an endpoint

.. code-block::
    
    dpai serve -p your_port

After the setup, you can call the endpoint or directly use the server as part of the backend services.